from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),
    path('add-project/', views.create_project, name='add-project'),
    path('edit-project/<str:pk>/', views.update_project, name='edit-project'),
    path('delete-project/<str:pk>/', views.delete_project, name='delete-project'),
    path('add-review/<str:pk>/', views.create_review, name='add-review'),
]