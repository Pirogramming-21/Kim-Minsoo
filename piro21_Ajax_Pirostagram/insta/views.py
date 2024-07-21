from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import PostForm, CommentForm
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def main(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    posts = Post.objects.filter(user=user).order_by('-created_at')
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    context = {
        'profile_user': user,
        'posts': posts,
        'posts_count': posts.count(),
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }
    
    return render(request, 'main.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse('insta:post_detail', kwargs={'post_id': post.id}))
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('insta:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'action': 'Update'})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('insta:post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'likes_count': post.likes.count(),
    }
    return render(request, 'post_detail.html', context)

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect(reverse('insta:main'))  # 메인 페이지로 리다이렉트
    return render(request, 'post_confirm_delete.html', {'post': post})

@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    
    user = request.user

    # 좋아요가 이미 있는지 확인
    like, created = Like.objects.get_or_create(user=user, post=post)
    
    if not created:
        # 좋아요가 이미 존재하면 삭제
        like.delete()
        liked = False
    else:
        # 좋아요가 존재하지 않으면 생성
        liked = True
    
    # 좋아요 수를 새로 계산
    likes_count = Like.objects.filter(post=post).count()

    return JsonResponse({'likes_count': likes_count, 'liked': liked})

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        
        return JsonResponse({
            'success': True,
            'id': comment.id,
            'username': comment.user.username,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)