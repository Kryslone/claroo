from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('create-course/', views.create_course, name='create_course'),
    path('course/', views.course_view, name='course'),
    path('teacher/home/', views.teacher_home, name='teacher_home'),
]