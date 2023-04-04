from django.contrib import admin
from .models import Person, Student, Hall, BoarderRoom
# Register your models here.

from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.contrib.admin import AdminSite, ModelAdmin
from .forms import PersonCreationForm, PersonChangeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

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

class StudentAdmin(ModelAdmin):
    model = Student
    
    def username(self, obj):
        return obj.person.username
    
    def first_name(self, obj):
        return obj.person.first_name
    
    def last_name(self, obj):
        return obj.person.last_name
    
    list_display = ('rollNumber', 'username', 'first_name', 'last_name')
    
class BoarderRoomInLine(admin.TabularInline):
    model = BoarderRoom
    readonly_fields = ('currentOccupancy',)
    
class BoarderRoomAdmin(ModelAdmin):
    model = BoarderRoom
    readonly_fields = ('currentOccupancy',)
    
    def name(self, obj):
        return obj.hall.name
    name.short_description = "Hall Name"
    
    list_display = ('name', 'roomNumber', 'rent', 'currentOccupancy', 'maxOccupancy', 'newstatus')
    
class HallAdmin(ModelAdmin):
    model = Hall
    inlines = [BoarderRoomInLine]
    readonly_fields = ('total_rooms',)
    
    def current_total_occupancy(self, obj):
        return obj.getCurrentOccupancy()
    def max_total_occupancy(self, obj):
        return obj.getMaxOccupancy()
    
    list_display = ('name', 'total_rooms', 'current_total_occupancy', 'max_total_occupancy')
    
    
admin.site.register(Person, PersonAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(BoarderRoom, BoarderRoomAdmin)

class HMCAdmin(AdminSite):
    site_header = "HMC Admin Area"
    
hmc_admin = HMCAdmin(name = "HMCAdmin")
hmc_admin.register(Student)
