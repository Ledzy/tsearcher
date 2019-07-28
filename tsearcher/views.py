from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from account.models import UserExtension

User = get_user_model()


def index(request):
    user = request.user
    context = {}
    context['user'] = user
    return render(request,'index.html',context)


def login_(request):
    if request.user.is_authenticated:
        return redirect('/account')

    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)
        print(username)
        if user is not None:
            print("login user")
            login(request,user)
            return redirect('/')

    return render(request,'login.html')

def signup_(request):
    if request.user.is_authenticated:
        return redirect('/account')

    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
        
        user = User.objects.create_user(username=username,password=password)
        user.save()
        login(request,user)
        return redirect('/')

    return render(request,'signup.html')