from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    


class User(AbstractUser):
    ROLES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='student')
    bio = models.TextField(blank=True)
    groups = models.ManyToManyField(Group, related_name='course_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='course_users', blank=True)

    def __str__(self):
        return self.username


class Course(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses',limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, blank=True, related_name='enrolled_courses', limit_choices_to={'role': 'student'})

    def __str__(self):
        return self.name

class Lesson(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Enrollment(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

class Quiz(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class Question(BaseModel):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class Answer(BaseModel):
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
