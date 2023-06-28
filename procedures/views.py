from django.shortcuts import render
from .models import CustomManager, User
from rest_framework.generics import GenericAPIView
from .serializers import SignupSerializer,LoginSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class Signup(GenericAPIView):
    serializer_class=SignupSerializer
    def post(self,request:Request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            phone_number = serializer.validated_data['phone_number']
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