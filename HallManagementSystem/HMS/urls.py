from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "hms-home"),
    path("register", views.register, name = "hms-register"),
]