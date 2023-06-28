from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate

class PhoneValidator(RegexValidator):
    regex = r'^\+?[1-9]\d{9}$'
    message = "Enter a valid phone number."

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[EmailValidator()])
    phone_number = serializers.IntegerField(validators=[PhoneValidator()])
    class Meta:
        model = User
        fields = ['email','username','password','phone_number']
    def validate(self, attrs):
        queryset=User.objects.all()
        email_exist=queryset.filter(email=attrs['email']).exists()
        if email_exist:
            raise ValidationError('Email has already been used')
        else:
            return super().validate(attrs)
        
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(validators=[EmailValidator()])
    password=serializers.CharField(style={'input-type':'password'})
    def validate(self,attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        if email and password:
            user=authenticate(email=email,password=password)
            if user:
                attrs['user']=user
            else:
                raise serializers.ValidationError('Invalid username or password')
        else:
            raise serializers.ValidationError('email and password are required')
        return attrs
    class Meta:
        model = User
        fields = ['email','password']