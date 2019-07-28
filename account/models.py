from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import Blog


# Create your models here.
class UserExtension(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="extension",parent_link=True)
    register_date = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    portrait = models.ImageField(null=True)
    phone = models.CharField(max_length=12,null=True)  #可以有更好的储存方式
    personal_info = models.TextField(max_length=150,null=True) #个人简介


@receiver(post_save,sender=User)
def handler_user_extension(sender,instance,created,**kwargs):
    if created:
        print("create new user")
        UserExtension.objects.create(user=instance)
    else:
        print("not created")
        instance.extension.save()