from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_task/', views.addTask, name='add_task'),
    path('view_task/<int:task_id>/', views.viewTask, name='view_task'),
    path('edit_task/<int:task_id>/', views.editTask, name='edit_task'),
    path('complete_task/<int:task_id>/', views.completeTask, name='complete_task'),
    path('delete_task/<int:task_id>/', views.deleteTask, name='delete_task'),
    path('edit_profile_view/', views.editProfileView, name='edit_profile_view'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]