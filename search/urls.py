from django.urls import path
from .views import search_page, query_teaching_plan, download_plan, query_slide, download_slide

app_name = 'search'

urlpatterns = [
    path('', search_page),
    path('download/teaching_plan/<int:file_index>',download_plan, name="download_plan"),
    path('download/slide/<int:file_index>',download_slide, name="download_plan"),
    path('teaching_plan/<str:query>', query_teaching_plan, name="query_teaching_plan"),
    path('slide/<str:query>', query_slide, name="query_slide"),
]