from django import forms
from .models import Post, Comment, User
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'profile_picture', 'website', 'password1', 'password2')
