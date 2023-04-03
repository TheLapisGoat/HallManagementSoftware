from django.contrib import admin
from .models import Person, Student

# Register your models here.
admin.site.register(Student)

from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.contrib.admin import AdminSite
from .forms import PersonCreationForm, PersonChangeForm
from django.contrib.auth.decorators import login_required

class PersonAdmin(UserAdmin):
    add_form = PersonCreationForm
    form = PersonChangeForm
    model = Person
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('is_staff', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'address', 'telephoneNumber', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'address', 'telephoneNumber', 'role', 'is_staff', 'is_superuser', 'groups')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

class CustomAdminSite(AdminSite):
    site_header = 'My Custom Admin Site'
    site_title = 'My Custom Admin Site'
    index_template = 'index-admin.html'
    
    def has_permission(self, request):
        if request.user.is_authenticated:
            return request.user.role == "admin"
        else:
            return False
        
    def login(self, request, extra_context=None):
        if not request.user.is_authenticated:
            return redirect('/login/')
        return super().login(request, extra_context)
    
custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(Person, PersonAdmin)

admin.site.register(Person, PersonAdmin)