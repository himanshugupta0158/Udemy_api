from django.contrib import admin
from .models import Courses , UserProfession

# Register your models here.

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ['title' , 'category' , 'Teacher_name' , 'price']

@admin.register(UserProfession)
class UserProfessionAdmin(admin.ModelAdmin):
    list_display = ['username' , 'profession']

