from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import PostForm, CommentForm, CustomUserCreationForm
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Prefetch


@login_required
def main(request):
    posts = Post.objects.all().order_by('-created_at')
    
    if request.user.is_authenticated:
        posts = posts.prefetch_related(
            Prefetch('likes', queryset=Like.objects.filter(user=request.user), to_attr='user_like')
        )
    
    context = {
        'posts': posts,
    }
    return render(request, 'main.html', context)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
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
    
    return render(request, 'profile.html', context)


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

    # 사용자가 이 게시물에 좋아요를 눌렀는지 확인
    user_likes_post = Like.objects.filter(user=request.user, post=post).exists()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'likes_count': post.likes.count(),
        'user_likes_post': user_likes_post,  # 추가된 부분
    }
    return render(request, 'post_detail.html', context)

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect(reverse('insta:main'))  
    return render(request, 'post_confirm_delete.html', {'post': post})

@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    likes_count = post.likes.count()

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

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('insta:main') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(
        Q(username__icontains=query) | Q(bio__icontains=query)
    )[:5]  # 최대 5명까지만 반환
    
    data = [{'username': user.username, 'profile_picture': user.profile_picture.url if user.profile_picture else None}
            for user in users]
    
    return JsonResponse(data, safe=False)

def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(caption__icontains=query) | Q(user__username__icontains=query)
    )[:5]  # 최대 5개까지만 반환
    
    data = [{
        'id': post.id,
        'caption': post.caption,
        'user': post.user.username,
        'image': post.image.url if post.image else None
    } for post in posts]
    
    return JsonResponse(data, safe=False)

@require_POST
def toggle_follow(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    user_to_follow = get_object_or_404(User, username=request.POST.get('username'))
    
    if request.user == user_to_follow:
        return JsonResponse({'error': 'You cannot follow yourself'}, status=400)
    
    follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    
    if not created:
        follow.delete()
        is_following = False
    else:
        is_following = True
    
    follower_count = user_to_follow.followers.count()
    
    return JsonResponse({
        'is_following': is_following,
        'follower_count': follower_count
    })

def logout_view(request):
    logout(request)
    return redirect('insta:main')  