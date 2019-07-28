from django.urls import path, re_path
from . import views

app_name = 'account'

urlpatterns = [
    path('',views.index),
    path('logout',views.logout_)
]