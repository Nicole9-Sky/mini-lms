from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, Comment, Review, Category
from .forms import CommentForm, UserProfileForm, ReviewForm, LessonForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages  # ✅ Added

# View to list all courses
def course_list(request):
    courses = Course.objects.all().order_by('-id')
    paginator = Paginator(courses, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses/courses_list.html', {'page_obj': page_obj})

# View for course detail and reviews
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all()
    reviews = course.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = ReviewForm()
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'reviews': reviews,
        'form': form
    })

# View to show all lessons with pagination
def lesson_list(request):
    lesson_list = Lesson.objects.all().order_by('id')
    paginator = Paginator(lesson_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses/lesson_list.html', {'page_obj': page_obj})

# View for individual lesson and comment
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    comments = Comment.objects.filter(lesson=lesson)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.lesson = lesson
            comment.user = request.user
            comment.save()
            return redirect('lesson_detail', lesson_id=lesson.id)
    else:
        form = CommentForm()

    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'comments': comments,
        'form': form,
    })

# Home page with search and category filtering
def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    courses = Course.objects.all()

    if query:
        courses = courses.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        courses = courses.filter(category__id=category_id)

    categories = Category.objects.all()
    paginator = Paginator(courses, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/home.html', {
        'courses': courses,
        'categories': categories,
        'page_obj': page_obj
    })

# Dashboard for tutors and students
@login_required
def dashboard(request):
    if request.user.is_tutor:
        courses = Course.objects.filter(tutor=request.user)
    else:
        courses = Course.objects.filter(enrollments__student=request.user)
    
    return render(request, 'courses/dashboard.html', {'courses': courses})

# User profile
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'courses/profile.html', {'form': form})

# ✅ UPDATED enroll view with success message
@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user.is_student:
        Enrollment.objects.get_or_create(student=request.user, course=course)
        messages.success(request, "✅ You successfully enrolled in the course!")  # ✅ Success Message
        return redirect('course_detail', course_id=course.id)
    else:
        return HttpResponse("Only students can enroll.", status=404)

# Secure lesson detail for enrolled students only
@login_required
def lesson_detail_secure(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    is_enrolled = Enrollment.objects.filter(course=course, student=request.user).exists()
    if not is_enrolled:
        return HttpResponseForbidden("You must be enrolled in this course to view the lessons.")

    return render(request, 'courses/lesson_detail.html', {'lesson': lesson, 'course': course})

# Add lesson to course (for tutors)
@login_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = LessonForm()

    return render(request, 'courses/add_lesson.html', {'form': form, 'course': course})

# Comment on a lesson
@login_required
def add_comment(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.student = request.user
            comment.lesson = lesson
            comment.save()
            return redirect('course_detail', course_id=lesson.course.id)
    else:
        form = CommentForm()
    return render(request, 'courses/add_comment.html', {'form': form, 'lesson': lesson})

# User registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_student = True
            user.save()
            login(request, user)
            return redirect('course_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# User login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return render(request, 'courses/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})

# User logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

        