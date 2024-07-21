from django.urls import path
from .views import *

app_name = 'insta'

urlpatterns = [
    path('', main, name='main'),
    path('create/', post_create, name='post_create'),
    path('/post/<int:post_id>/', post_detail, name='post_detail'),
    path('update/<int:post_id>/', post_update, name='post_update'),
    path('delete/<int:post_id>', post_delete, name='post_delete'),
    path('like/', like_post, name='like_post'),
    path('posts/<int:post_id>/add_comment/', add_comment, name='add_comment'),
    path('comments/delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),

]