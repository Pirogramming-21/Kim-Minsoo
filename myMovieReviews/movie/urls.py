from django.urls import path
from .views import *

app_name = 'movie'

urlpatterns = [
    path('', review_list),
    path('detail', review_detail),
    path('create', review_create),
]