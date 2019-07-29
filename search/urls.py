from django.urls import path
from .views import search_page, query_info, download

app_name = 'search'

urlpatterns = [
    path('', search_page),
    path('download/<int:file_index>',download, name="download"),
    path('<str:query>', query_info, name="query_info"),
]