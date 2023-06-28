from rest_framework import serializers
from .models import User,Blog,like
from rest_framework.validators import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueTogetherValidator


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

class CreateListBlogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title=serializers.CharField(max_length=30)
    content=serializers.CharField(max_length=30)
    description=serializers.CharField(max_length=180)
    def validate(self, attrs):
        if not attrs.get('title'):
            raise serializers.ValidationError("Title cannot be empty.")
        if not attrs.get('content'):
            raise serializers.ValidationError("Content cannot be empty.")
        if not attrs.get('description'):
            raise serializers.ValidationError("Description cannot be empty.")
        return attrs
    class Meta:
        model = Blog
        fields = ['id','title','content','description']

class Blogs(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    class Meta:
        model=Blog
        fields=['id','title','content','description','total_likes']
    def get_total_likes(self, obj):
        return obj.post.count()

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    class Meta:
        model = like
        fields = ['blog','user']
        validators = [
            UniqueTogetherValidator(
                queryset=like.objects.all(),
                fields=['blog', 'user'],
                message='This blog is already liked by the You.'
            )
        ]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','phone_number']