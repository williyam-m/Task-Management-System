from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Task
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
import os

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    user_model = User.objects.get(username=request.user.username)
    user = Profile.objects.get(user=user_model)
    tasks = Task.objects.filter(Q(created_by=user_model.id) | Q(assigned_to=user_model.email)).distinct()

    pending_tasks = tasks.filter(status='pending')
    completed_tasks = tasks.filter(status='completed')

    context = {
        'user' : user,
        'total_tasks': tasks.count(),
        'pending_tasks': pending_tasks.count(),
        'completed_tasks': completed_tasks.count(),
        'pending_task_list': pending_tasks,
        'completed_task_list': completed_tasks,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def completeTask(request, task_id):
    task = Task.objects.get(id=task_id)


    if task.assigned_to == request.user.email:
        task.status = 'completed'
        task.completed_date = timezone.now().date()

        task.save()

    return redirect('dashboard')


@login_required(login_url='login')
def deleteTask(request, task_id):
    task = Task.objects.get(id=task_id)

    if task.created_by.username == request.user.username:
        task.delete()

    return redirect('dashboard')


@login_required(login_url='login')
def addTask(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        task_description = request.POST['task_description']
        assigned_to = request.POST['assigned_to']
        priority = request.POST['priority']
        due_date = request.POST['due_date']


        # only current or future dates
        if due_date < datetime.now().strftime('%Y-%m-%d'):
            messages.info(request, 'Date must be valid')
            return redirect('/add_task/')


        user_model = User.objects.get(username=request.user.username)

        task = Task.objects.create(created_by = user_model, task_name=task_name, assigned_to=assigned_to, task_description=task_description, priority = priority, due_date= due_date)
        task.save()
        return redirect('dashboard')

    today = datetime.now().strftime('%d-%m-%Y')
    return render(request, 'add_task.html', {'today': today})


@login_required(login_url='login')
def editTask(request, task_id):
    task = Task.objects.get(id=task_id)

    if task.created_by.username != request.user.username:
        return redirect('dashboard')

    if request.method == 'POST':
        task_name = request.POST['task_name']
        task_description = request.POST['task_description']
        assigned_to = request.POST['assigned_to']
        priority = request.POST['priority']
        due_date = request.POST['due_date']


        # only current or future dates
        if due_date < datetime.now().strftime('%Y-%m-%d'):
            messages.info(request, 'Date must be valid')
            return redirect('/edit_task/' + str(task_id) + '/')

        user_model = User.objects.get(username=request.user.username)


        task.task_name=task_name
        task.assigned_to = assigned_to
        task.task_description = task_description
        task.priority = priority
        task.due_date = due_date
        task.save()
        return redirect('dashboard')

    return render(request, 'edit_task.html', {'task' : task})

@login_required(login_url='login')
def viewTask(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'view_task.html', {'task': task})


@login_required(login_url='login')
def editProfileView(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)

        if profile.profile_img and profile.profile_img != "blank-profile-picture.jpg":
            if len(profile.profile_img) > 0:
                os.remove(profile.profile_img.path)

        profile.profile_img = request.FILES['profile_img']
        profile.save()

        return redirect('dashboard')
    return render(request, 'profile_image.html')


def home(request):

  return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/register')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/register')

            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()


                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)


                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('/register')

    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/login')

    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)

    return redirect('/login')
