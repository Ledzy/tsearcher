from django.db import models
from django.contrib.auth.models import User

if len(User.objects.filter(username="Internet"))==0:
    default_user = User.objects.create_user(username="Internet")
else:
    default_user = User.objects.filter(username="Internet")[0]


class Subject(models.Model):
    type_name = models.CharField(max_length=20)
    slide_count = models.IntegerField(null=True)
    plan_count = models.IntegerField(null=True)

    def __str__(self):
        return self.type_name



#教案
class TeachingPlan(models.Model):
    uploader = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="teaching_plans",null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    filename = models.TextField()
    content = models.TextField()
    index = models.IntegerField() #索引
    star = models.IntegerField() #评分，0-5


class Slides(models.Model):
    uploader = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="slides",null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    first_page = models.ImageField(null=True)
    filename = models.TextField()
    index = models.IntegerField() #索引
    star = models.IntegerField() #评分，0-5