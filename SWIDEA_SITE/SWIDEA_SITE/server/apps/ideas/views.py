from django.shortcuts import render, redirect, get_object_or_404
from .models import Idea
from .forms import *
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Case, When, BooleanField
import json

def idea_list(req):   
  sort_option = req.GET.get('sort', 'created')  # 기본 정렬 옵션은 등록순
  if sort_option == 'likes':
    # starred가 True인 항목을 먼저 정렬하고, 그 다음에 나머지 항목을 정렬
    ideas = Idea.objects.annotate(
        is_starred=Case(
            When(starred=True, then=True),
            default=False,
            output_field=BooleanField()
        )
    ).order_by('-is_starred', 'created_at')
  elif sort_option == 'name':
      ideas = Idea.objects.all().order_by('name')  # 이름순
  elif sort_option == 'updated':
      ideas = Idea.objects.all().order_by('-updated_at')  # 최신순
  else:
      ideas = Idea.objects.all().order_by('created_at')  # 등록순

  ctx = {
    'ideas': ideas
  }

  return render(req, 'ideas/list.html', ctx)

def idea_create(req):
  if req.method == 'POST':
    form = IdeaForm(req.POST, req.FILES)
    if form.is_valid():
      form.save()
      return redirect('ideas:idea_list')
  else:
    form = IdeaForm()

  ctx = {
    'form': form
  }
  return render(req, 'ideas/create.html', ctx)

def idea_detail(req, pk):
  idea = get_object_or_404(Idea, id=pk)
  ctx = {
    'idea': idea
  }
  return render(req, 'ideas/detail.html', ctx)

def idea_update(req, pk):
  idea = get_object_or_404(Idea, pk=pk)
  if req.method == 'POST':
    form = IdeaForm(req.POST, req.FILES, instance=idea)
    if form.is_valid():
      form.save()
      return redirect('ideas:idea_detail', pk=idea.pk)
  else:
    form = IdeaForm(instance=idea)

  ctx = {
    'form': form,
    'idea': idea,
  }
  return render(req, 'ideas/update.html', ctx)

def idea_delete(req, pk):
  idea = get_object_or_404(Idea, id=pk)
  if req.method == "POST":
    idea.delete()
    return redirect('ideas:idea_list')
  
@require_POST
def update_interest(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    data = json.loads(request.body)
    action = data.get('action')

    if action == 'increase':
        idea.interest += 1
    elif action == 'decrease':
        idea.interest = max(0, idea.interest - 1)
    
    idea.save()

    return JsonResponse({'success': True, 'new_value': idea.interest})

@require_POST
def toggle_star(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    data = json.loads(request.body)
    idea.starred = data.get('starred', False)
    idea.save()
    return JsonResponse({'success': True, 'starred': idea.starred})