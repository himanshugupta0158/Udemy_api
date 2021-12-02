from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password , check_password

from django.views.decorators.csrf import csrf_exempt

from rest_framework import mixins
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
        CourseSerializer,
        CartSerializer
                          )
from .models import Courses , UserProfession , Cart

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
            UserProfession(username = request.data['username'], profession = request.data['profession']).save()
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
    queryset = Courses.objects.all()
    
    @csrf_exempt
    def get(self, request):
        course = self.get_queryset()
        serializer = self.get_serializer(course , many = True)
        return Response(serializer.data , status = status.HTTP_200_OK)

class Upload(GenericAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Courses
    
    @csrf_exempt
    def get(self, request):
        user = UserProfession.objects.get(username = request.user.username)
        if user.profession == 'Teacher' :
            return Response({"Upload allowed" : "Teacher are allows to upload video(s)."} , status = status.HTTP_400_BAD_REQUEST)
        else :
            return Response({"Upload not allowed" : "Students are not allows to upload video(s)."} , status = status.HTTP_400_BAD_REQUEST)
    
    
    @csrf_exempt
    def post(self, request):
        user = UserProfession.objects.get(username = request.user.username)
        if user.profession == 'Teacher' :
            serializer = self.get_serializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status = status.HTTP_200_OK)
            return Response({"Upload failed" : "video does not uploaded."} , status = status.HTTP_400_BAD_REQUEST)
        else :
            return Response({"Upload failed" : "Students are not allows to upload video(s)."} , status = status.HTTP_400_BAD_REQUEST)


class Category(GenericAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Courses
    
    @csrf_exempt
    def get(self , request):
        java = set()
        python = set()
        kotlin = set()
        other = set()
        
        for i in Courses.objects.all():
            if i.category == 'Python' :
                python.add(i)
            elif i.category == 'Java' :
                java.add(i)
            elif i.category == 'Kotlin':
                kotlin.add(i)
            else:
                other.add(i)
        data = {
            'Python' : python ,
            'Java' : java ,
            'Kotlin' : kotlin , 
            'other' : other
        }
        
        serializer = CourseSerializer(data = data , many = True)
        if serializer.is_valid():
            return Response(serializer.data , status = status.HTTP_200_OK)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    
    


class AddToCart(GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    @csrf_exempt
    def get(self, request ,id):
        course = Courses.objects.get(id = id)
        item = {
            'course_title' : course.title,
            'access_name' : request.user.username
        }
        serializer = self.get_serializer(data= item)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status = status.HTTP_200_OK)
        return Response({"Process failed" : "Course does not added to cart"} , status = status.HTTP_400_BAD_REQUEST)
    
    
class CartItem(GenericAPIView ,mixins.ListModelMixin , mixins.RetrieveModelMixin , mixins.DestroyModelMixin):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Cart
    
    @csrf_exempt
    def get(self, request):
        items = Cart.objects.filter(access_name = request.user.username)
        course = dict()
        print(course)
        for item in items :
            course['item'] = Courses.objects.get(title = item.course_title)
        print(course)
        serializer = CourseSerializer(data = course)
        print(serializer)
        if serializer.is_valid():
            print('valid')
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
            
            
            
class DeleteCartItem(GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    lookup_field = 'id'
        
    @csrf_exempt
    def get(self, request , id = None):
        try:
            if request.user.username == Cart.objects.get(id = id).access_name :
                return self.retrieve(request)
            else :
                return Response({'access failed' : 'unauthorized access failed.'} , status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'not found' : 'Item does not exist'} , status = status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self , request , id):
        try:
            if request.user.username == Cart.objects.get(id = id).access_name :
                return self.destroy(request , id)
            return Response({'access failed' : 'unauthorized access failed.'} , status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'not found' : 'Item does not exist'} , status = status.HTTP_400_BAD_REQUEST)

    
    
        

