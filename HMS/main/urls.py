from django.contrib import admin
from django.urls import path, include
from . import views
from .admin import custom_admin_site

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home", views.index, name = "index"),
    path("", views.index, name = "index"),
    path("login/", views.loginUser, name="main-login"),
    path("logout/", views.logoutUser, name = "main-logout"),
    path("custom-admin/", custom_admin_site.urls, name = "main-customadmin"),
]