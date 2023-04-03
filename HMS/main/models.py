from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "profile")
    
    address = models.TextField()
    telephoneNumber = models.IntegerField()
    #photograph = models.ImageField()
    
    def __str__(self):
        return self.user.username

class Allocation(models.Model):
    name = models.CharField(max_length = 100)
    allocated_grant = models.FloatField()

    def __str__(self):
        return self.name
    
    def change_value(self, value):
        self.allocated_grant = value
        self.save()

class Expense(models.Model):
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
    allocations = models.ForeignKey(Allocation, on_delete=models.PROTECT)
    #hallPhoto = models.ImageField()
    
    def __str__(self):
        return self.allocations #dont know what to return here
    
    def get_total(self):
        return - self.expenses - self.pettyexpenses + self.allocations
    
    def get_petty_expenses(self):
        return self.pettyexpenses
    
    def get_allocations(self):
        return self.allocations