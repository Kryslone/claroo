from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm
from .models import CourseGroup, Profile, Student, Teacher
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Course
import json

# Create your views here.

def index(response):
    return render(response, "claroapp/base_simple.html", {})

@login_required
def home(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'full_name': f"{request.user.first_name} {request.user.last_name}",
        'email': request.user.email
    }
    
    if profile.role == 'student':
        return render(request, 'claroapp/student/s_home.html', context)
    elif profile.role == 'teacher':
        return render(request, 'claroapp/teacher/t_home.html', context)
    else:
        return render(request, 'claroapp/home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.
            return render(request, 'claroapp/auth/login.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'claroapp/auth/login.html')
    
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = Profile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                role=form.cleaned_data['role']
            )
            if profile.role == 'student':
                Student.objects.create(profile=profile)
            elif profile.role == 'teacher':
                Teacher.objects.create(profile=profile)
            login(request, user)
            return redirect('home')  # Redirect to a success page.
        else:
            # Debugging: Print form errors
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'claroapp/auth/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# views.py
@login_required
def create_course(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            teacher = Teacher.objects.get(profile__user=request.user)
            
            # Create course
            course = Course.objects.create(
                name=data['courseName'],
                description=data.get('description', ''),  # Make description optional
                code=data.get('section', ''),  # Use section as code
                teacher=teacher
            )
            
            # Create associated group
            course_group = CourseGroup.objects.create(course=course)
            
            return JsonResponse({
                'success': True,
                'course': {
                    'id': course.id,
                    'name': course.name,
                    'description': course.description,
                    'code': course.code,
                    'section': course.code,
                    'room': data.get('room', ''),
                    'groupId': course_group.id
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def course_view(request):
    context = {
        'full_name': f"{request.user.first_name} {request.user.last_name}",
        'email': request.user.email
    }
    return render(request, 'claroapp/teacher/t_course.html', context)

def teacher_home(request):
    return render(request, 'claroapp/teacher/t_home.html')