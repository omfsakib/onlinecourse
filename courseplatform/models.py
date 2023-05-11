from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Address(BaseModel):
    detail_address = models.TextField(max_length=2000, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)


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
    
    
class UserProfile(Address):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username


class Course(BaseModel):
    _name = models.CharField(max_length=200)
    _description = models.TextField()
    _start_date = models.DateField()
    _end_date = models.DateField()
    _teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses',limit_choices_to={'role': 'teacher'})
    _students = models.ManyToManyField(User, blank=True, related_name='enrolled_courses', limit_choices_to={'role': 'student'})

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, value):
        self._teacher = value

    @property
    def students(self):
        return self._students

    @students.setter
    def students(self, value):
        self._students = value

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
    
    def __str__(self):
        return self.title

class Question(BaseModel):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
        
    def __str__(self):
        return self.text

class Answer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    @staticmethod
    def is_correct_answer(id):
        try:
            answer = Answer.objects.get(id=id)
            if answer.is_correct:
                return True
            else:
                return False
        except Answer.DoesNotExist:
            return False
    
    def __str__(self):
        return self.question.text