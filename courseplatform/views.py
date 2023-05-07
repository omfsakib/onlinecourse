from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages


# Public Views
def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        print('Working')
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('courseplatform:course_list')
        else:
            print(form.errors)
    else:
        form = SignUpForm(request.POST)
    
    context = {
        'form' : form,
    }
    return render(request, 'registration/signup_form.html',context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('courseplatform:course_list')
        else:
            # Return an error message if authentication fails
            error_message = "Invalid username or password. Please try again."
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'registration/login.html')


class CourseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'
    permission_required = ('courses.view_private_course',)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.has_perm('courses.view_private_course'):
            qs = qs.filter(is_private=False)
        return qs

def CourseDetailView(request,pk):
    course = get_object_or_404(Course, pk=pk)
    total_entrollment = course.students.all().count()
    
    lessons = Lesson.objects.filter(course = course)
    total_lessons = lessons.count()
    
    total_quiz = 0
    for i in lessons:
        total_quiz += Quiz.objects.filter(lesson=i).count()

    
    context = {
        'course' : course,
        'total_entrollment':total_entrollment,
        'lessons':lessons,
        'total_lessons':total_lessons,
        'total_quiz' :total_quiz
    }
    return render(request,'course_detail.html',context)

def LessonsPreview(request,pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    quizes = Quiz.objects.filter(lesson = lesson)
    total_quizes = quizes.count()    
    
    # print(total_quizes)
    
    context = {
        'lesson' : lesson,
        'quizes' :quizes,
        'total_quizes': total_quizes
    }
    return render(request,'lesson_preview.html',context)


def StartQuiz(request,pk):
    quiz = get_object_or_404(Quiz, pk =pk)
    questions = Question.objects.filter(quiz = quiz)
    
    if request.method == "POST" and 'question_id' in request.POST:
        question_id = request.POST.get('question_id')
        question = Question.objects.get(id = question_id)
        answer = request.POST.get('answer')
        answer_obj = Answer.objects.create(user = request.user, question = question)
        answer_obj.text = answer
        answer_obj.save()
        
        return redirect('courseplatform:answers')
        
        
    context = {
        'quiz' : quiz,
        'questions' :questions,
    }
    return render(request,'quiz_start.html',context)


def SeeAnswers(request):
    user = request.user
    answers =  Answer.objects.filter(user = user)
    
    if request.method == "POST" and 'answer_id' in request.POST:
        answer_id = request.POST.get('answer_id')
        is_correct = Answer.is_correct_answer(answer_id)
        print(is_correct)
        
        context = {
            'is_correct' : is_correct,
            'answers':answers
        }
    else:
        context = {
            'answers':answers
        }
    return render(request,'answers.html',context)
# Student Views

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    Enrollment.objects.create(student=request.user, course=course)
    return render(request, 'enroll_success.html', {'course': course})


@login_required
def my_courses(request):
    my_enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'my_courses.html', {'enrollments': my_enrollments})


@staff_member_required
class CourseUpdateView(UpdateView):
    model = Course
    fields = ['title', 'description', 'category', 'level', 'price', 'image']
    template_name = 'course_form.html'


@staff_member_required
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course_confirm_delete.html'
    success_url = reverse_lazy('instructor_dashboard')


@staff_member_required
class LessonCreateView(CreateView):
    model = Lesson
    fields = ['title', 'description', 'video_url']
    template_name = 'lesson_form.html'

    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.kwargs['course_pk'])
        return super().form_valid(form)


@staff_member_required
class LessonUpdateView(UpdateView):
    model = Lesson
    fields = ['title', 'description', 'video_url']
    template_name = 'lesson_form.html'


@staff_member_required
class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'lesson_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})


