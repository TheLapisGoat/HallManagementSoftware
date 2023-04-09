from django.contrib import admin
from .models import Person, Student, Hall, BoarderRoom, MessAccount, MessManager, Passbook, Due, AmenityRoom, Complaint, ComplaintRegister, Warden, HallClerk, HallEmployee, HallEmployeeLeave, UserPayment, HallPassbook, PettyExpense, SalaryExpense, ATR
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
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'address', 'photograph', 'telephoneNumber', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'address', 'telephoneNumber', 'first_name', 'last_name', 'photograph', 'role', 'is_staff', 'is_superuser', 'groups')}
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
    
    list_display = ('roomNumber', 'name', 'rent', 'currentOccupancy', 'maxOccupancy', 'newstatus')

class AmenityRoomAdmin(ModelAdmin):
    model = AmenityRoom
    
    def hall(self, obj):
        return obj.hall.name
    
    list_display = ('name', 'hall', 'roomNumber', 'rent',)  

class WardenAdmin(ModelAdmin):
    model = Warden
    add_form = WardenCreationForm
    
    def name(self, obj):
        return obj.person.get_full_name()
    
    list_display = ('name', 'hall')
    
class ATRAdmin(ModelAdmin):
    model = ATR
    list_display = ('title', 'complaint', 'details', 'date' )
    
class HallAdmin(ModelAdmin):
    model = Hall
    inlines = [BoarderRoomInLine,AmenityRoomInLine]
    readonly_fields = ('total_boarderrooms','total_amenityrooms',)
    
    def current_total_occupancy(self, obj):
        return obj.getCurrentOccupancy()
    def max_total_occupancy(self, obj):
        return obj.getMaxOccupancy()
    
    list_display = ('name', 'total_boarderrooms', 'total_amenityrooms', 'current_total_occupancy', 'max_total_occupancy')
    
class DueAdmin(ModelAdmin):
    model = Due
    
    def passbook(self, obj):
        return str(obj.passbook)
    
    list_display = ('demand', 'passbook', 'type', 'timestamp')
    
class HallClerkAdmin(ModelAdmin):
    model = HallClerk
    
    def name(self, obj):
        return obj.person.get_full_name()
    
    list_display = ('name', 'hall')
    
class HallEmployeeLeaveAdmin(ModelAdmin):
    model = HallEmployeeLeave
    
    def employee(self, obj):
        return obj.hallemployee.name
    employee.short_description = "Hall Employee Name"
    
    def hall(self, obj):
        return obj.hallemployee.hall.name
    
    list_display = ('employee', 'hall', 'date')
    
class HallEmployeeAdmin(ModelAdmin):
    model = HallEmployee
    
    def daily_salary(self, obj):
        return obj.salary
    
    list_display = ('name', 'hall', 'job', 'daily_salary')
    
class MessAccountAdmin(ModelAdmin):
    model = MessAccount
    
    def hall(self, obj):
        return obj.student.hall.name
    
    def name(self, obj):
        return obj.student.person.get_full_name()
    name.short_description = "Student Name"
        
    list_display = ("name", 'hall', 'due')
    
class MessManagerAdmin(ModelAdmin):
    model = MessManager
    
    def name(self, obj):
        return obj.person.get_full_name()
    
    list_display = ('name', 'hall')
    
class PassbookAdmin(ModelAdmin):
    model = Passbook
    
    def rollNumber(self, obj):
        return obj.student.rollNumber
    
    def name(self, obj):
        return obj.student.person.get_full_name()
    
    list_display = ('rollNumber', 'name',)

class PettyExpenseAdmin(ModelAdmin):
    model = PettyExpense
    
    def hall(self, obj):
        return obj.passbook.hall.name
    
    list_display = ('description', 'hall', 'demand', 'timestamp')
    
class SalaryExpenseAdmin(ModelAdmin):
    model = SalaryExpense
    
    def hall(self, obj):
        return obj.passbook.hall.name
    
    list_display = ('name', 'job', 'hall', 'demand', 'timestamp')
    
admin.site.register(Person, PersonAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(BoarderRoom, BoarderRoomAdmin)
admin.site.register(AmenityRoom, AmenityRoomAdmin)
admin.site.register(MessAccount, MessAccountAdmin)
admin.site.register(Passbook, PassbookAdmin)
admin.site.register(Due, DueAdmin)
admin.site.register(MessManager, MessManagerAdmin)
admin.site.register(Complaint)
admin.site.register(ComplaintRegister)
admin.site.register(Warden, WardenAdmin)
admin.site.register(HallClerk, HallClerkAdmin)
admin.site.register(HallEmployee, HallEmployeeAdmin)
admin.site.register(HallEmployeeLeave, HallEmployeeLeaveAdmin)
admin.site.register(UserPayment)
admin.site.register(HallPassbook)
admin.site.register(ATR,ATRAdmin)
admin.site.register(PettyExpense, PettyExpenseAdmin)
admin.site.register(SalaryExpense, SalaryExpenseAdmin)

admin.site.site_header = 'Hall Management System Administration'
