from django.contrib import admin
from .models import Person, Student

# Register your models here.
admin.site.register(Student)

from django.contrib.auth.admin import UserAdmin
from .forms import PersonCreationForm, PersonChangeForm

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

admin.site.register(Person, PersonAdmin)