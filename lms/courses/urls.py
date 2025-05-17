from django.urls import path 
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('lesson/<int:lesson_id>/comment/', views.add_comment, name='add_comment'),
    path("course/<int:course_id>/lesson/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"), 
    
    
    path('courses/', views.course_list, name='courses'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('course/<int:course_id>/add_lesson/', views.add_lesson, name='add_lesson'),
    path('course/<int:course_id>/lesson/int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('lessons/', views.lesson_list, name='lesson_list'),
]
