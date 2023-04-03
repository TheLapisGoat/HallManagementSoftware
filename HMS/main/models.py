from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
# Create your models here.

class Person(AbstractUser, PermissionsMixin):
    
    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"
    address = models.TextField("Address")
    telephoneNumber = models.IntegerField("TelephoneNumber")
    #photograph = models.ImageField("Photo")

    REQUIRED_FIELDS = ["email", "address", "telephoneNumber"]
    
class Student(models.Model):
    person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "student", primary_key = True)
    #roomNumber = models.ForeignKey()

class Warden(models.Model):
    person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "warden", primary_key = True)
    #IAMAWARDEN
    
class Hall(models.Model):
    name = models.CharField(max_length = 100)
    total_rooms  = models.IntegerField()
    
    # messManager = models.OneToOneField(MessManager, on_delete = models.CASCADE, related_name = "messManager")
    #not in the class diagram and changed it locally
    # warden = models.OneToOneField(Warden, on_delete = models.CASCADE, related_name = "warden")
    # expenditure = models.OneToOneField(HallBudget, on_delete = models.CASCADE, related_name = "expenditure")
    
class ComplaintRegister(models.Model):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "complaintRegister")
    
    
class Complaint(models.Model):
    ComplaintRegister = models.ForeignKey(ComplaintRegister, on_delete = models.CASCADE, related_name = "complaints")
    details = models.CharField()
    date = models.DateField()
    nameagainst = models.CharField()
    #image = models.ImageField()
    status = models.CharField(max_length = 100)

class ATR(models.Model):
    name = models.CharField(max_length = 100)
    details = models.CharField()
    complaint = models.ForeignKey(Complaint, on_delete = models.CASCADE, related_name = "ATR")
    
    def __str__(self):
        return self.title
    
    def change_status(self, status):
        self.status = status
        self.save()


class Expense(models.Model):        # change expense-hallbudget relation to aggregation
    name = models.CharField(max_length = 100)
    cost = models.FloatField()
    
    def __str__(self):
        return self.name
   
    def change_value(self, value):
        self.cost = value
        self.save()

class HallBudget(models.Model):
    hall = models.OneToOneField(Hall, on_delete = models.CASCADE, related_name = "hallBudget")
    expenses = models.ForeignKey(Expense, on_delete=models.PROTECT)     # PROTECT raises ProtectedError when Expense object is deleted
    pettyexpenses = models.ForeignKey(Expense, on_delete=models.PROTECT)
    # allocations = models.ForeignKey(Allocation, on_delete=models.PROTECT)
    #hallPhoto = models.ImageField()
    
    def __str__(self):
        return self.allocations #dont know what to return here
    
    def get_total(self):
        return - self.expenses - self.pettyexpenses + self.allocations
    
    def get_petty_expenses(self):
        return self.pettyexpenses
    
    def get_allocations(self):
        return self.allocations

class Allocation(models.Model):     # change allocation-hallbudget relation to aggregation
    hall_budget= models.ForeignKey(HallBudget, on_delete = models.CASCADE, related_name = "allocations")
    name = models.CharField(max_length = 100)
    allocated_grant = models.FloatField()

    def __str__(self):
        return self.name
    
    def change_value(self, value):
        self.allocated_grant = value
        self.save()

class Room(models.Model):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "rooms")
    roomNumber = models.CharField(max_length = 100)
    rent = models.FloatField()
    
    def __str__(self):
        return self.roomNumber
    
    def get_rent(self):
        return self.rent
    
    class Meta:
        abstract = True
    
class AmenityRoom(Room):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "amenityRooms")
    amenity_name = models.CharField(max_length = 100)

    def get_amenity_name(self):
        return self.amenity_name
    
class BoarderRoom(Room):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "boarderRooms")
    occupancyNumber = models.IntegerField()
    # boarders?
    newstatus = models.BooleanField(default = False)
    currentnoStudents = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.roomNumber
    
    def get_occupancy_number(self):
        return self.occupancyNumber
