from django.urls import path
from .import views

urlpatterns = [
    path('signup/',views.Signup.as_view(),name='UserSignup'),
    path('login/',views.Login.as_view(),name='Login'),
    path('blog/',views.CreateListBlog.as_view(),name='Blog'),
]