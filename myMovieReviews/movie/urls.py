from django.urls import path
from .views import *

app_name = 'movie'

urlpatterns = [
    path('', review_list, name='movie_detail'),
    path('detail/<int:pk>/', review_detail),
    path('create', review_create),
    path('detail/<int:pk>/update/', review_update),
    path('detail/<int:pk>/delete/', review_delete),

]