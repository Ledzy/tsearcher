from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import UserExtension

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		context = {}
		if hasattr(request.user,'extension'):
			ue = request.user.extension
		else:
			ue = UserExtension.objects.create(user=request.user)
		context['ue'] = ue

		return render(request,'my-profile.html',context)

	else:
		return redirect('login')

def logout_(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')