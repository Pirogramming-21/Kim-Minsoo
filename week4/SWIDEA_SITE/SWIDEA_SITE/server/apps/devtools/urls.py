from django.urls import path
from . import views

app_name = 'devtools'

urlpatterns = [
  path('', views.devtool_list, name='devtool_list'),
  path('create/', views.devtool_create, name='devtool_create'),
  path('detail/<int:pk>', views.devtool_detail, name='devtool_detail'),
  path('update/<int:pk>', views.devtool_update, name='devtool_update'),
  path('delete/<int:pk>', views.devtool_delete, name='devtool_delete'),
]