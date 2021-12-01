from django.db import models

# Create your models here.

# adding new course

class Courses(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length = 150)
    created_on = models.DateTimeField(auto_now_add=True)
    Teacher_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    video = models.FileField(upload_to='media/')
