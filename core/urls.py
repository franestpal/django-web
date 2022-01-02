from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from .views import (
SignUpView,LoginView)



urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('signup/', SignUpView.as_view(), name="signup"),


]
   
    


