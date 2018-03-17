from django.contrib import admin
from django.urls import path
from app_proyecto import views
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    path('admin/', admin.site.urls), #Administraciòn por defecto
]
