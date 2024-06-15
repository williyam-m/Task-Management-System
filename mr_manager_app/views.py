from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.

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
