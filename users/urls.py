from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('account/', views.account, name='account'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('edit-profile/', views.update_profile, name='edit-profile'),
    path('delete-account/', views.delete_profile, name='delete-account'),
    path('add-skill/', views.create_skill, name='add-skill'),
    path('edit-skill/<str:pk>/', views.update_skill, name='edit-skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete-skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.message, name='message'),
    path('send-message/<str:pk>/', views.create_message, name='send-message'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
]
