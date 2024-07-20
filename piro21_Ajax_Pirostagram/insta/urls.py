from django.urls import path
from .views import *

app_name = 'insta'

urlpatterns = [
    path('', main, name='main'),
    path('create/', post_create, name='post_create'),
    path('/post/<int:post_id>/', post_detail, name='post_detail'),
    path('update/<int:post_id>/', post_update, name='post_update'),
    path('delete/<int:post_id>', post_delete, name='post_delete'),

]