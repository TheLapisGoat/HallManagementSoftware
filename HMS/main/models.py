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
