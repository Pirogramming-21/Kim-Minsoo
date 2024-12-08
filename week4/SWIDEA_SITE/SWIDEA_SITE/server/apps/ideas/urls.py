from django.urls import path
from . import views

app_name = 'ideas'

urlpatterns = [
  path('', views.idea_list, name='idea_list'),
  path('create', views.idea_create, name='idea_create'),
  path('detail/<int:pk>', views.idea_detail, name='idea_detail'),
  path('update/<int:pk>', views.idea_update, name='idea_update'),
  path('delete/<int:pk>', views.idea_delete, name='idea_delete'),
  path('<int:idea_id>/update-interest/', views.update_interest, name='update_interest'),
  path('<int:idea_id>/toggle-star/', views.toggle_star, name='toggle_star'),
]