from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#forms
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
#temp
from django.http import HttpResponse

def vlogin(request):
    context = {
        'form': LoginForm()
    }
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.data['username']
            password = loginform.data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) #надо будет messages прикрутить
                return HttpResponse('<h2>Вы успешно вошли в свой аккаунт!<h2>')
            else:
                return redirect('login')
    return render(request, 'login.html', context)


def vregister(request):
    pass


@login_required
def vlogout(request):
    logout(request)
    return HttpResponse('<h2>Вы успешно вышли из аккаунта!</h2>') #temp, later redirect on index
