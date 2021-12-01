from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password , check_password

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication , SessionAuthentication , BasicAuthentication

from django.core.files.storage import FileSystemStorage

from .serializers import ( 
        UserSerializer, 
        RegisterSerializer , 
        LoginSerializer , 
        ChangePasswordSerializer ,
        CourseSerializer
                          )
from .models import Courses

# Create your views here.

# Register API
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = [SessionAuthentication]
    # authentication_classes = [TokenAuthentication]
    
    @csrf_exempt    
    def post(self , request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request , user)
            return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)

            
# Login API
class Login(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = [SessionAuthentication]
    
    def get_object(self , username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist :
            return None
    
    @csrf_exempt    
    def post(self , request):
        user = self.get_object(request.data.get("username"))
        flag = check_password(request.data.get("password") , user.password)
        if not user:
            return Response({'Not Found' : 'User does not exist'} , status = status.HTTP_400_BAD_REQUEST)
        elif flag : 
            login(request , user)
            return Response({'Logged in' : 'User Logged in Successfully. '})
        else :
            return Response({'Wrong passwrd' : 'User password does not matched'} , status = status.HTTP_400_BAD_REQUEST)

# Logout API
class Logout(GenericAPIView):
    serializer_class = LoginSerializer       
    authentication_classes = [SessionAuthentication]
    
    def get(self , request):
        logout(request)
        return Response({'Logging out' : 'User Logged out Successfully. '})

# Reset Password API
class ResetPasswordAPI(GenericAPIView):
    serializer_class = LoginSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    # authentication_classes = [TokenAuthentication]
    
    def get_object(self , username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist :
            return None
        
    @csrf_exempt        
    def post(self , request):
        user = self.get_object(request.data.get("username"))
        if not user :
            return Response({'Not Found' : 'User does not exist'} , status = status.HTTP_400_BAD_REQUEST)
        data = {
            "password" : make_password(request.data.get("password"))
            }
        serializer = self.get_serializer(user , data = data , partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordAPI(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    # authentication_classes = [TokenAuthentication]    
    
    def get_object(self , username ):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist :
            return None
    
    @csrf_exempt    
    def post(self , request):
        if request.user.username == request.data.get("username") :
            user = self.get_object(request.data.get("username"))
            flag = check_password(request.data.get("password") , user.password)
            if user is None :
                return Response({'Not Found' : 'User does not exist'} , status = status.HTTP_400_BAD_REQUEST)
            elif flag : 
                data = {
                    "password" : make_password(request.data.get("new_password"))
                }
                serializer = self.get_serializer(user , data = data , partial = True)
                if serializer.is_valid():
                    user = serializer.save()
                    return Response({"user": UserSerializer(user).data})
                return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : "old password not match"} , status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Invalid Username" : "For changing password logged in username should be use."})


class Dashboard(GenericAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Courses
    
    @csrf_exempt
    def get(self, request):
        course = Courses.objects.all()
        serializer = self.get_serializer(course , many = True)
        return Response(serializer.data , status = status.HTTP_200_OK)

class Upload(GenericAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Courses
    
    @csrf_exempt
    def post(self, request):
        data = request.data
        
        title  = data.get('title') , 
        video = request.FILES['video'] , 
        description = data.get('description') , 
        category =  data.get('category') , 
        Teacher_name = data.get('Teacher_name') , 
        price = data.get('price')
        
        fss = FileSystemStorage()
        fss.save(video.name , video)
        
        upload = {
            'title' : title ,
            'video' : video ,
            'description' : description , 
            'category' : category ,
            'Teacher_name' : Teacher_name ,
            'price' : price
        }
        
        
        serializer = self.get_serializer(data = upload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status = status.HTTP_200_OK)
        return Response({"Upload failed" : "video does not uploaded."} , status = status.HTTP_400_BAD_REQUEST)
            
    
        

