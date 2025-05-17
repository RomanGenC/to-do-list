from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_page, name='base-page'),
    path('login/', views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('register/', views.register, name='register'),

    path('create_task/', views.create_task, name='create_task'),
    path('all-tasks/', views.get_user_tasks, name='all_tasks'),
    path('task-detail/<int:pk>/', views.task_detail, name='task_detail'),
]
