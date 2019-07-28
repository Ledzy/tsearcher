from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request,'my-profile.html')
        
    else:
        return redirect('login')

def logout_(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')