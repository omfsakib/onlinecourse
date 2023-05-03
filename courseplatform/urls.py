from django.urls import path
from .views import *
from . import views
app_name = 'courseplatform'

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/',CourseDetailView.as_view(), name='course_detail'),
    path('register/', views.signup, name='register'),
]