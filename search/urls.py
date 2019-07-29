from django.urls import path
from .views import search_page, query_info

app_name = 'search'

urlpatterns = [
    path('', search_page),
    path('<str:query>', query_info, name="query_info")
]