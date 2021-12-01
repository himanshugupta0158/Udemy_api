from rest_framework import serializers
# from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Courses

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'email']

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
            max_length=100,min_length=6,write_only=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
    
    def create(self , validated_data):
        if validated_data['password']!=validated_data['confirm_password']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        # password = make_password(validated_data['password'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'password']

class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
            max_length=100,min_length=6,write_only=True)
    class Meta:
        model = User
        fields = ['username' , 'password' , 'new_password']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['title' , 'category' , 'description' , 'Teacher_name' , 'created_on' , 'price' , 'video']
