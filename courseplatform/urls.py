from django.urls import path
from .views import *
from . import views
app_name = 'courseplatform'

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/',views.CourseDetailView, name='course_detail'),
    path('courses/lesson/<int:pk>/',views.LessonsPreview, name='lesson_preview'),
    path('courses/lesson/quiz/<int:pk>/',views.StartQuiz, name='start_quiz'),
    path('answers/', views.SeeAnswers, name='answers'),
    path('register/', views.signup, name='register'),
    path('login/', views.login_view, name='login'),
]