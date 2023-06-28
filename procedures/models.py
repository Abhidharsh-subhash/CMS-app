from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

#custom manager for user
class CustomManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        for i in extra_fields:
            print(i)
        email=self.normalize_email(email)
        user=self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
class User(AbstractUser):
    email=models.CharField(max_length=80,unique=True)
    username=models.CharField(max_length=45)
    phone_number=models.IntegerField()

    objects=CustomManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    
class Blog(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    title=models.CharField(max_length=30)
    content=models.CharField(max_length=30)
    description=models.CharField(max_length=180)
    creation_date=models.DateField(auto_now_add=True)

    def __init__(self):
        return self.title


