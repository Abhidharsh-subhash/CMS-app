from rest_framework import serializers
from .models import User,Blog,like,Comments
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
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(max_length=12, write_only=True)
    repeatpassword = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Enter confirm password',
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        queryset=User.objects.all()
        email_exist=queryset.filter(email=attrs['email']).exists()
        password=attrs['password']
        repeatpassword=attrs['repeatpassword']
        if password != repeatpassword:
            raise ValidationError('Password mismatch.')
        if email_exist:
            raise ValidationError('Email has already been used.')
        else:
            return super().validate(attrs)
        
    class Meta:
        model = User
        fields = ['email','phone_number','username','password','repeatpassword']
        
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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['user','blog','comment']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','phone_number']