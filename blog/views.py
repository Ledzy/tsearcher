from django.shortcuts import render, render_to_response
from .models import Blog

# Create your views here.
def single_post(request):
    context = {} #你需要把变量传到context去，然后在html里面调用
    return render(request,'single-post.html',context)