from django.contrib import admin
from django.urls import path,include
from . import views
from users import views as user_views
from django.urls import path

urlpatterns = [
    path('', user_views.home, name='home'),
    path('register/',user_views.register,name='register'),
    path('login/',user_views.loginUser, name='login'),
    path('logout/', user_views.logoutUser, name='logout')
]