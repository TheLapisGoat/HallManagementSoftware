from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Person(AbstractUser, PermissionsMixin):
    
    first_name = models.CharField("first name", max_length=150, blank=False)
    last_name = models.CharField("last name", max_length=150, blank=False)
    email = models.EmailField("email address", blank=False)
    
    ROLES = [
        ('student', 'Student'),
        ('warden', 'Warden'),
        ('hall_clerk', 'Hall Clerk'),
        ('hmc_chairman', 'HMC Chairman'),
        ('mess_manager', 'Mess Manager'),
        ('admin', 'Administrator'),
        ('admission', 'Admission Unit'),
    ]
    
    role = models.CharField("Role", max_length=40, choices=ROLES, default='student', blank = False)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"
        
    address = models.TextField("Address", blank=False)
    telephoneNumber = PhoneNumberField("Telephone Number", blank=False)
    photograph = models.ImageField("Photo", blank = True)

    REQUIRED_FIELDS = ["email", "address", "telephoneNumber", "role", "first_name", "last_name"]
    
class Hall(models.Model):
    name = models.CharField("Name", max_length = 100, blank = False, primary_key = True)
    total_boarderrooms  = models.IntegerField("Total Boarder Rooms", default = 0, blank = False)
    total_amenityrooms  = models.IntegerField("Total Amenity Rooms", default = 0, blank = False)
    
    def __str__(self):
        return self.name
          
    def getCurrentOccupancy(self):
        return self.boarderRooms.aggregate(total = Sum('currentOccupancy'))['total']
    
    def getMaxOccupancy(self):
        return self.boarderRooms.aggregate(total = Sum('maxOccupancy'))['total']
    
class HallClerk(models.Model):
    person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "hall_clerk", primary_key = True, blank = False, unique = True)
    hall = models.OneToOneField(Hall, on_delete = models.PROTECT, related_name = "hall_clerk", blank = False, unique = True)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(HallClerk, self).save(*args, **kwargs)
            self.person.role = 'hall_clerk'
        else:
            self.person.role = 'hall_clerk'
            super(HallClerk, self).save(*args, **kwargs)
            
    def __str__(self):
        return self.person.first_name

class HallEmployee(models.Model):
    name = models.CharField("Name", max_length = 100, blank = False)
    hall = models.ForeignKey(Hall, on_delete = models.PROTECT, related_name = "hall_employees", blank = False)
    job = models.CharField("Job", max_length = 100, blank = False)
    salary = models.DecimalField("Salary", default = 0, blank = False, max_digits = 8, decimal_places = 2)
    
    def __str__(self):
        return self.name
    
class HallEmployeeLeave(models.Model):
    hallemployee = models.ForeignKey(HallEmployee, on_delete = models.CASCADE, related_name = "leaves", blank = False)
    date = models.DateField("Date", blank = False)

class MessManager(models.Model):
    person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "mess_manager", primary_key = True, blank = False, unique = True)
    hall = models.OneToOneField(Hall, on_delete = models.PROTECT, related_name = "mess_maanger", blank = False, unique = True)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(MessManager, self).save(*args, **kwargs)
            self.person.role = 'mess_manager'
        else:
            self.person.role = 'mess_manager'
            super(MessManager, self).save(*args, **kwargs)
            
    def __str__(self):
        return self.person.first_name + self.person.last_name

class Room(models.Model):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "rooms", blank = False)
    roomNumber = models.CharField("Room Number", max_length = 100, blank = False)
    rent = models.DecimalField("Rent", default = 0, blank = False, max_digits = 8, decimal_places = 2)
    
    def __str__(self):
        return self.roomNumber    
    class Meta:
        abstract = True
        
class AmenityRoom(Room):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "amenityRooms", blank = False)
    name = models.CharField("Name", max_length = 100, blank = False)
        
    def __str__(self):
        return self.roomNumber + " - " + self.name

class BoarderRoom(Room):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "boarderRooms", blank = False)
    newstatus = models.BooleanField("New Status", blank = False, default = True)
    maxOccupancy = models.IntegerField("Max Occupancy", blank = False)
    currentOccupancy = models.IntegerField("Current Occupancy", blank = False, default = 0)
    
    def __str__(self):
        return self.roomNumber + " - " + self.hall.name + "|" + str(self.currentOccupancy) + "/" + str(self.maxOccupancy)
    
class Student(models.Model):
    person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "student", primary_key = True, blank = False, unique = True)
    hall = models.ForeignKey(Hall, on_delete = models.PROTECT, related_name = "students", blank = False)
    rollNumber = models.CharField("Roll Number", max_length = 100, blank = False, unique = True)
    room = models.ForeignKey(BoarderRoom, on_delete = models.PROTECT, related_name = "students", blank = False)
    
    def __str__(self):
        return self.person.first_name + " " + self.person.last_name + " - " + self.rollNumber

class Warden(models.Model):
    person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "warden", primary_key = True)
    hall = models.OneToOneField(Hall, on_delete = models.PROTECT, related_name = "warden", blank = False, unique = True)
    
    def __str__(self):
        return self.person.first_name + " " + self.person.last_name + " - " + self.hall.name

class MessAccount(models.Model):
    student = models.OneToOneField(Student, on_delete = models.CASCADE, related_name = "messAccount", blank = False, primary_key = True, unique = True)
    due = models.DecimalField("Mess Due", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    paid = models.DecimalField("Paid", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    last_update = models.DateTimeField("Last Update Date", auto_now = True)
    
    def __str__(self):
        return "Mess Account: " + self.student.person.first_name + " " + self.student.person.last_name + " - " + self.student.rollNumber
    
class Passbook(models.Model):
    student = models.OneToOneField(Student, on_delete = models.CASCADE, related_name = "passbook", blank = False, primary_key = True, unique = True)

    def __str__(self):
        return "Passbook: " + self.student.person.first_name + " " + self.student.person.last_name + " - " + self.student.rollNumber
    
class Due(models.Model):
    
    TYPE = [
        ('mess', 'Mess Due'),
        ('boarderRoom', 'Boarder Room Due'),
        ('amenityRooms', 'Amenity Rooms Due'),
    ]
    
    timestamp = models.DateTimeField("Timestamp", blank = False, auto_now_add = True)
    demand = models.DecimalField("Demand", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    type = models.CharField("Type", max_length = 100, choices = TYPE, blank = False, default = 'mess')
    passbook = models.ForeignKey(Passbook, on_delete = models.CASCADE, related_name = "dues", blank = False)
    
    def __str__(self):
        return  self.type + ":" + self.passbook.student.person.first_name + " " + self.passbook.student.person.last_name + " - " + self.passbook.student.rollNumber
    
class Payment(models.Model):
    
    timestamp = models.DateTimeField("Timestamp", blank = False, auto_now_add = True)
    fulfilled = models.DecimalField("Fulfilled", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    passbook = models.ForeignKey(Passbook, on_delete = models.CASCADE, related_name = "payments", blank = False)
    
class ComplaintRegister(models.Model):
    hall = models.OneToOneField(Hall, on_delete = models.CASCADE, related_name = "complaint_register", blank = False, primary_key = True)
        
    def __str__(self):
        return self.hall.name
            
class Complaint(models.Model):
    complaintregister = models.ForeignKey(ComplaintRegister, on_delete = models.CASCADE, related_name = "r_complaints")
    student = models.ForeignKey(Student, on_delete = models.CASCADE, related_name = "s_complaints")
    title = models.CharField(max_length = 100)
    description = models.TextField()
    date = models.DateField()
    nameagainst = models.CharField(max_length = 100)
    status = models.CharField(max_length = 100, default = "Pending")    
    #image = models.ImageField()

class ATR(models.Model):
    name = models.CharField(max_length = 100)
    details = models.TextField()
    complaint = models.OneToOneField(Complaint, on_delete = models.CASCADE, related_name = "ATR", blank = False, primary_key = True)

    def change_status(self, status):
        self.status = status
        self.save()             

class HallPassbook(models.Model):
    hall = models.OneToOneField(Hall, on_delete = models.CASCADE, related_name = "passbook", blank = False, primary_key = True, unique = True)

class Expense(models.Model):
    
    timestamp = models.DateTimeField("Timestamp", blank = False, auto_now = True)
    demand = models.DecimalField("Demand", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    class Meta:
        abstract = True
    
class PettyExpense(Expense):
    description = models.CharField("Description", max_length = 100, blank = False)
    passbook = models.ForeignKey(HallPassbook, on_delete = models.CASCADE, related_name = "pettyexpenses", blank = False)
    
class SalaryExpense(Expense):
    name = models.CharField("Name", max_length = 100, blank = False)
    job = models.CharField("Job", max_length = 100, blank = False)
    passbook = models.ForeignKey(HallPassbook, on_delete = models.CASCADE, related_name = "salaryexpenses", blank = False)

class UserPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

class ATR(models.Model):
    title = models.CharField(max_length = 100)
    details = models.TextField()
    complaint = models.OneToOneField(Complaint, on_delete = models.CASCADE, related_name = "ATR", blank = False, primary_key = True)
    date = models.DateField()

@receiver(post_save, sender=Student)
def create_student_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(student=instance)