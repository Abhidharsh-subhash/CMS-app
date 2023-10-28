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
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    email = models.CharField(max_length=80,unique=True)
    username = models.CharField(max_length=45)
    phone_number = models.IntegerField(null=True)

    objects=CustomManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='writer')
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=30)
    description = models.CharField(max_length=180)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id
    
class like(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='post')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')

    def __str__(self):
        return f"Likes: {self.blog.likes.count()} - {self.blog.title}"

class Comments(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comblog')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comuser')
    comment = models.TextField()

    def __str__(self):
        return f"user : {self.user.email} - comment : {self.comment}"


