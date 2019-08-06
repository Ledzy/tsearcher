from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from account.models import UserExtension
from blog.models import Blog
from search.models import Subject
import random

User = get_user_model()
blog_display = 5
user_display = 6

def index(request):
    context = {}
    user = request.user
    subjects = Subject.objects.all()
    newest_blogs = Blog.objects.order_by('-created_time')[:blog_display]
    hotest_blogs = Blog.objects.order_by('-created_time')[:blog_display]

    context['request_user'] = user
    context['ue'] = UserExtension.objects.all()[:user_display]
    context['hotest_blogs'] = hotest_blogs
    context['newest_blogs'] = newest_blogs
    context['subjects'] = subjects
    return render(request,'index.html',context)

def about(request):
    return render(request,'about.html')


def contact_us(request):
    context['subjects'] = subjects
    return render(request,'contact.html')


def login_(request):
    if request.user.is_authenticated:
        return redirect('/account')

    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)
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
        
        user = User.objects.create_user(username=username,password=password)
        user.save()
        login(request,user)
        return redirect('/')

    return render(request,'signup.html')