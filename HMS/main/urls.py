from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/", admin.site.index, name = "admin-index"),
    path("home", views.index, name = "index"),
    path("", views.index, name = "index"),
    path("login/", views.loginUser, name="main-login"),
    path("logout/", views.logoutUser, name = "main-logout"),
    path("admission/", views.admissionIndex, name = "admission-index"),
    path("admission/new_admission/", views.newAdmission, name = "newadmission"),
    path("messmanager/", views.messManagerIndex, name = "messmanager-index"),
    path("messmanager/manage_accounts/", views.manageMessAccounts, name = "manage-mess-accounts"),
    path("home/complaints", views.complaints, name = "complaints-student"),
    path("home/newcomplaints", views.newComplaints, name = "newcomplaints-student"),
    path("home/newwarden", views.newWarden, name = "newwarden"),
    path("passbook/", views.passbook, name = "passbook"),
    path("passbook/pay", views.pay, name = "pay"),
    path("hallclerk/", views.hallClerkIndex, name = "hallclerk-index"),
    path('hallclerk/<int:pk>/edit/', views.edit_hallemployee, name = "edit-hallemployee"),
    path('hallclerk/<int:pk>/leaves/', views.leaves_hallemployee, name='leaves-hallemployees'),
    path('hallclerk/<int:pk>/add_leave/', views.add_hallemployee_leave, name='add-leave-hallemployee'),
    path('hallclerk/add_hallemployee/', views.add_hallemployee, name='add-hallemployee'),
    path('hallclerk/<int:pk>/delete/', views.delete_hallemployee, name='delete-hallemployee'),
    path("passbook/pay/success", views.payment_successful, name = "success"),
    path("passbook/pay/cancel", views.payment_cancelled, name = "cancel"),
    path("passbook/pay/stripe_webhook/", views.stripe_webhook, name = "stripe_webhook"),
    path("warden/", views.wardenIndex, name = "warden-index"),
    path("warden/calculate_student_fees/", views.calculate_student_fees, name = "calculate-student-fees"),
    path("warden/<str:pk>/confirmstudentfees/", views.confirm_student_fees, name = "confirm-student-fees"),
    path("hmcchairman/", views.chairmanIndex, name = "hmcchairman-index"),
    path("hmcchairman/generate_mess_report", views.generate_mess_report, name = "mess-report"),
    path('warden/generate_salaries/', views.generate_monthly_salary, name = "generate-salaries"),
    path('warden/generate_salary_report/', views.generate_monthly_salary_report, name = "generate-salary-report"),
    path('warden/hallpassbook/', views.hallpassbook, name = "hallpassbook"),
    path('hallclerk/add_pettyexpense/', views.add_pettyexpense, name = "add-pettyexpense"),
]