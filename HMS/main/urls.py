from django.contrib import admin
from django.urls import path, include
from . import views
from .admin import hmc_admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home", views.index, name = "index"),
    path("", views.index, name = "index"),
    path("login/", views.loginUser, name="main-login"),
    path("logout/", views.logoutUser, name = "main-logout"),
    path("hmcadmin", hmc_admin.urls),
    path("admission/", views.admissionIndex, name = "admission-index"),
    path("admission/new_admission/", views.newAdmission, name = "newadmission"),
    path("messmanager/", views.messManagerIndex, name = "messmanager-index"),
    path("messmanager/manage_accounts/", views.manageMessAccounts, name = "manage-mess-accounts"),
]