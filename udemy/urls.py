from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('resetpassword/', views.ResetPasswordAPI.as_view(), name='resetpassword'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('changepassword/', views.ChangePasswordAPI.as_view(), name='changepassword'),
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path("upload/", views.Upload.as_view(), name="upload"),
    path("addtocart/<int:id>", views.AddToCart.as_view(), name="addtocart"),
    path("cart/", views.CartItem.as_view(), name="cart"),
    path("cart/<int:id>", views.DeleteCartItem.as_view()),
    path("category/", views.Category.as_view(), name="category"),
    
]