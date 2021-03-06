from django.contrib import admin
from .models import Courses , UserProfession , Cart

# Register your models here.

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ['title' , 'id' , 'category' , 'Teacher_name' , 'price']

@admin.register(UserProfession)
class UserProfessionAdmin(admin.ModelAdmin):
    list_display = ['username' , 'profession']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['access_name' , 'course_title']

