from django.urls import path
from .views import *

app_name = 'insta'

urlpatterns = [
    path('', index, name='index'),
]