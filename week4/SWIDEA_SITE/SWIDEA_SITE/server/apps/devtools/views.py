from django.shortcuts import render, redirect, get_object_or_404
from .models import DevTool
from .forms import *

def devtool_list(req):
  devtools = DevTool.objects.all()
  ctx = {
    'devtools': devtools
  }
  return render(req, 'devtools/list.html', ctx)

def devtool_create(req):
  if req.method == 'POST':
    form = DevToolForm(req.POST, req.FILES)
    if form.is_valid():
      form.save()
      return redirect('devtools:devtool_list')
  else:
    form = DevToolForm()

  ctx = {
    'form': form
  }
  return render(req, 'devtools/create.html', ctx)

def devtool_detail(req, pk):
  devtools = get_object_or_404(DevTool, id=pk)
  ideas = devtools.ideas.all()
  ctx = {
    'devtools': devtools,
    'ideas': ideas
  }
  return render(req, 'devtools/detail.html', ctx)

def devtool_update(req, pk):
  devtools = get_object_or_404(DevTool, pk=pk)
  if req.method == 'POST':
    form = DevToolForm(req.POST, req.FILES, instance=devtools)
    if form.is_valid():
      form.save()
      return redirect('devtools:devtool_detail', pk=devtools.pk)
  else:
    form = DevToolForm(instance=devtools)

  ctx = {
    'form': form,
    'devtools': devtools,
  }
  return render(req, 'devtools/update.html', ctx)

def devtool_delete(req, pk):
  devtools = get_object_or_404(DevTool, id=pk)

  if req.method == 'POST':
    devtools.delete()
    return redirect('devtools:devtool_list')
  return redirect('devtools:devtool_list')
