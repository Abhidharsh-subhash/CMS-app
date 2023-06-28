from django.urls import path
from .import views

urlpatterns = [
    path('signup/',views.Signup.as_view(),name='signup'),
    path('login/',views.Login.as_view(),name='login'),
    path('blog/',views.CreateListBlog.as_view(),name='blog'),
    path('blogs/',views.AllBlogs.as_view(),name='blogs'),
    path('like/',views.likeBlogs.as_view(),name='like'),
    path('profile/',views.profile.as_view(),name='profile'),
    path('userlist/',views.Userlist.as_view(),name='userlist'),
]