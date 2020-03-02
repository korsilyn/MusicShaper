from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#forms
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
#for debug only
from django.http import HttpResponse

def login_page(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.data['username']
            password = loginform.data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) #надо будет messages прикрутить
                return redirect('index')
            else:
                return redirect('login')
        else:
            return redirect('login')
    else:
        context = {
            'form': LoginForm()
        }
        return render(request, 'login.html', context)


def register_page(request):
    if request.method == 'POST':
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            regform.save()
            username = regform.data['username']
            password = regform.data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) #надо будет messages прикрутить
                return redirect('index')
            else:
                return redirect('register')
        else:
            return redirect('register')
    else:
        context = {
            'form': UserCreationForm()
        }
        return render(request, 'register.html', context)


@login_required
def logout_page(request):
    logout(request)
    return redirect('index')
