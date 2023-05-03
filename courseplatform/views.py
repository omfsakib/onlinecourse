from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
    


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson_detail.html'


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
