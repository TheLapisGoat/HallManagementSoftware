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
