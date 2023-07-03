from django.shortcuts import render
from .models import User,Blog
from rest_framework.generics import GenericAPIView
from .serializers import SignupSerializer,LoginSerializer,CreateListBlogSerializer,Blogs,LikeSerializer,ProfileSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# Create your views here.

class Signup(GenericAPIView):
    serializer_class=SignupSerializer
    def post(self,request:Request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            # data = serializer.validated_data
            # password = data.pop('password')  # Removing 'password' from the dictionary
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            phone_number = serializer.validated_data['phone_number']
            # user = User.objects.create(**data)
            user=User.objects.create(
                email=email,
                username=username,
                phone_number=phone_number,
            )
            user.set_password(password)
            user.save()
            response={
                'status':201,
                'message':'User created successfully'
                }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response={
                'status':400,
                'message':'Enter valid credentials'
            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
        
class Login(GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.validated_data['user']
            token=RefreshToken.for_user(user)
            response={
            'status':200,
            'message':'User login successful',
            'access':str(token.access_token),
            'refresh':str(token)
            }
            return Response(data=response,status=status.HTTP_200_OK)
        else:
            response={
                'status':400,
                'message':'Invalid credentials'
            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)

class CreateListBlog(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CreateListBlogSerializer
    def post(self,request):
        user=request.user
        data=request.data
   
        serializer=self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data['title']
            content = serializer.validated_data['content']
            description = serializer.validated_data['description']
            blog=Blog.objects.create(
                user=user,
                title=title,
                content=content,
                description=description
            )
            blog.save()
            response={
                'status':201,
                'message':'Blog created successfully'
                }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response={
                'status':400,
                'message':'Enter valid credentials'
            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(user=user)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        pk = request.data.get('postid')
        try:
            blog = Blog.objects.get(user=user, pk=pk)
        except:
            blog=None

        if blog:
            blog.delete()
            response = {
                'status': 200,
                'message': 'Blog deleted successfully'
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                'status': 404,
                'message': 'Blog not found'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        user = request.user
        data = request.data
        pk = request.data.get('postid')
        blog = Blog.objects.get(user=user, pk=pk)

        if blog:
            serializer = self.serializer_class(blog, data=data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    'status': 200,
                    'message': 'Blog updated successfully'
                }
                return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                'status': 404,
                'message': 'Blog not found'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        
class AllBlogs(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=Blogs
    queryset=Blog.objects.all()
    def get(self,request):
        serializer=self.serializer_class(self.get_queryset(),many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class likeBlogs(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=LikeSerializer
    def post(self,request):
        user=request.user
        data = {'user': user.id, 'blog': request.data.get('blog')}
        context = {'request': request}
        serializer=self.serializer_class(data=data,context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'status': 201,
                'message': 'Blog liked successfully'
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response = {
            'status': 400,
            'message': 'Invalid request',
            'errors': serializer.errors
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

class profile(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ProfileSerializer
    def get(self,request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    def patch(self,request):
        user=request.user
        serializer=self.serializer_class(user,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response={
                'status':200,
                'message':'Profile Updated suceessfully'
            }
            return Response(data=response,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Userlist(GenericAPIView):
    serializer_class=ProfileSerializer
    queryset=User.objects.all()
    def get(self,request):
        serializer=self.serializer_class(self.get_queryset(),many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    