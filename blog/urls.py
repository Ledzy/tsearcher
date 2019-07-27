from django.urls import path
from .views import single_post

urlpatterns = [
    path('',single_post)
    ]