from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse



# Create your views here.


def Checklogin(request):
    if request.user.is_authenticated:

        return redirect(reverse('index'))
    else:
        return redirect(reverse('login'))


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect(reverse('index'))
        else:

            return redirect(reverse('register'))

    else:

        return render(request, template_name='login.html')


def register(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        login(request, user)

        return redirect(reverse('index'))

    else:
        return render(request, template_name='register.html')


def Logout(request):
    logout(request)
    return redirect(reverse('login'))



def Delete_Account(request):
    user = User.objects.get(username=request.user.username)
    user.delete()
    return HttpResponseRedirect('/')




@login_required(login_url='/login')
def Index(request):
    user_name = request.user.username
    return render(request, template_name='index.html', context={"name": user_name})
