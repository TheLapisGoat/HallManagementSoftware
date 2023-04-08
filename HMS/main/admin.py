from django.contrib import admin
from .models import Person, Student, Hall, BoarderRoom, MessAccount, MessManager, Passbook, Due, AmenityRoom, Complaint, ComplaintRegister, Warden, UserPayment
# Register your models here.

from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.contrib.admin import AdminSite, ModelAdmin
from .forms import PersonCreationForm, PersonChangeForm, StudentCreationForm, StudentChangeForm, WardenCreationForm

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
    add_form = StudentCreationForm
    form = StudentChangeForm
    
    def username(self, obj):
        return obj.person.username
    
    def first_name(self, obj):
        return obj.person.first_name
    
    def last_name(self, obj):
        return obj.person.last_name
    
    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)
    
    list_display = ('rollNumber', 'username', 'first_name', 'last_name')
    
class BoarderRoomInLine(admin.TabularInline):
    model = BoarderRoom
    readonly_fields = ('currentOccupancy',)

class AmenityRoomInLine(admin.TabularInline):
    model = AmenityRoom
    
class BoarderRoomAdmin(ModelAdmin):
    model = BoarderRoom
    readonly_fields = ('currentOccupancy',)
    
    def name(self, obj):
        return obj.hall.name
    name.short_description = "Hall Name"
    
    list_display = ('name', 'roomNumber', 'rent', 'currentOccupancy', 'maxOccupancy', 'newstatus')

class AmenityRoomAdmin(ModelAdmin):
    model = AmenityRoom
    
    def name(self, obj):
        return obj.hall.name
    name.short_description = "Hall Name"
    list_display = ('name', 'roomNumber', 'rent',)  

class WardenAdmin(ModelAdmin):
    model = Warden
    add_form = WardenCreationForm
    list_display = ('person', 'hall')
    
class HallAdmin(ModelAdmin):
    model = Hall
    inlines = [BoarderRoomInLine,AmenityRoomInLine]
    readonly_fields = ('total_boarderrooms','total_amenityrooms',)
    
    def current_total_occupancy(self, obj):
        return obj.getCurrentOccupancy()
    def max_total_occupancy(self, obj):
        return obj.getMaxOccupancy()
    
    list_display = ('name', 'total_boarderrooms', 'total_amenityrooms', 'current_total_occupancy', 'max_total_occupancy')
     
        
admin.site.register(Person, PersonAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(BoarderRoom, BoarderRoomAdmin)
admin.site.register(AmenityRoom, AmenityRoomAdmin)
admin.site.register(MessAccount)
admin.site.register(Passbook)
admin.site.register(Due)
admin.site.register(MessManager)
admin.site.register(Complaint)
admin.site.register(ComplaintRegister)
admin.site.register(Warden,WardenAdmin)
admin.site.register(UserPayment)

class HMCAdmin(AdminSite):
    site_header = "HMC Admin Area"
    
hmc_admin = HMCAdmin(name = "HMCAdmin")
hmc_admin.register(Student)