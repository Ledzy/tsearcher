from django.contrib import admin
from .models import Subject, TeachingPlan, Slides

# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('type_name','slide_count','plan_count')

@admin.register(TeachingPlan)
class TeachingPlanAdmin(admin.ModelAdmin):
    list_display = ('filename','uploader','subject')