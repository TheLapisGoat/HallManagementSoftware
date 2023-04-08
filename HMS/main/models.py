from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models import Sum
# Create your models here.

class Person(AbstractUser, PermissionsMixin):
    
    ROLES = [
        ('student', 'Student'),
        ('warden', 'Warden'),
        ('hall_clerk', 'Hall Clerk'),
        ('hmc_chairman', 'HMC Chairman'),
        ('mess_manager', 'Mess Manager'),
        ('admin', 'Administrator'),
        ('admission', 'Admission Unit'),
        ('hall_clerk', 'Hall Clerk')
    ]
    
    role = models.CharField("Role", max_length=40, choices=ROLES, default='student', blank = False)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"
        
    address = models.TextField("Address", blank=False)
    telephoneNumber = models.IntegerField("TelephoneNumber", blank=False)
    #photograph = models.ImageField("Photo")

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

class HallEmployee(models.Model):
    name = models.CharField("Name", max_length = 100, blank = False)
    hall = models.ForeignKey(Hall, on_delete = models.PROTECT, related_name = "hall_employees", blank = False)
    job = models.CharField("Job", max_length = 100, blank = False)
    salary = models.DecimalField("Salary", default = 0, blank = False, max_digits = 8, decimal_places = 2)
    
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

class Room(models.Model):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "rooms", blank = False)
    roomNumber = models.CharField("Room Number", max_length = 100, blank = False)
    rent = models.FloatField("Rent", default = 0, blank = False)
    
    def __str__(self):
        return self.roomNumber    
    class Meta:
        abstract = True
        
class AmenityRoom(Room):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "amenityRooms", blank = False)
    name = models.CharField("Name", max_length = 100, blank = False)
        
    def __str__(self):
        return self.name

class BoarderRoom(Room):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "boarderRooms", blank = False)
    newstatus = models.BooleanField("New Status", blank = False, default = True)
    maxOccupancy = models.IntegerField("Max Occupancy", blank = False)
    currentOccupancy = models.IntegerField("Current Occupancy", blank = False, default = 0)
    
class Student(models.Model):
    person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "student", primary_key = True, blank = False, unique = True)
    hall = models.ForeignKey(Hall, on_delete = models.PROTECT, related_name = "students", blank = False)
    rollNumber = models.CharField("Roll Number", max_length = 100, blank = False, unique = True)
    room = models.ForeignKey(BoarderRoom, on_delete = models.PROTECT, related_name = "students", blank = False)

class Warden(models.Model):
    person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "warden", primary_key = True)
    hall = models.OneToOneField(Hall, on_delete = models.PROTECT, related_name = "warden", blank = False, unique = True)

   

# class Fees(models.Model):
#     student = models.OneToOneField(Student, on_delete = models.CASCADE, related_name = "fees")
#     amenityFees = models.FloatField()
#     roomFees = models.FloatField()
#     def getAmenityFees(self):
#         return self.amenityFees
#     def getRoomFees(self):
#         return self.roomFees

class MessAccount(models.Model):
    student = models.OneToOneField(Student, on_delete = models.CASCADE, related_name = "messAccount", blank = False, primary_key = True, unique = True)
    due = models.DecimalField("Mess Due", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    paid = models.DecimalField("Paid", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    last_update = models.DateField("Last Update Date", auto_now_add = True)
    
class Passbook(models.Model):
    student = models.OneToOneField(Student, on_delete = models.CASCADE, related_name = "passbook", blank = False, primary_key = True, unique = True)

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
    
class Payment(models.Model):
    
    timestamp = models.DateTimeField("Timestamp", blank = False, auto_now_add = True)
    fulfilled = models.DecimalField("Fulfilled", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    passbook = models.ForeignKey(Passbook, on_delete = models.CASCADE, related_name = "payments", blank = False)
    
class ComplaintRegister(models.Model):
    hall = models.OneToOneField(Hall, on_delete = models.CASCADE, related_name = "complaint_register", blank = False, primary_key = True)
        
    def __str__(self):
        return self.hall.name
        
    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         super(ComplaintRegister, self).save(*args, **kwargs)
    #         self.save()
    #         self.hall.save()
    #     else:
    #         super(ComplaintRegister, self).save(*args, **kwargs)
    #         self.hall.save()
            
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

# class HallBudget(models.Model):
#     hall = models.OneToOneField(Hall, on_delete = models.CASCADE, related_name = "hallBudget")
#     #allocations = models.ForeignKey(Allocation, on_delete=models.PROTECT)
#     #hallPhoto = models.ImageField()
#     # def __str__(self):
#     #     return self.allocations #dont know what to return here
#     # def get_total(self):
#     #     return - self.expenses - self.pettyexpenses + self.allocations
#     # def get_petty_expenses(self):
#     #     return self.pettyexpenses
#     # def get_allocations(self):
#     #     return self.allocations  

# class Expense(models.Model):        # change expense-hallbudget relation to aggregation
#     name = models.CharField(max_length = 100)
#     cost = models.FloatField()
#     hallbudget = models.ForeignKey(HallBudget, on_delete=models.CASCADE, related_name = "expenses") 
#     def __str__(self):
#         return self.name
   
#     def change_value(self, value):
#         self.cost = value
#         self.save()
        
# class PettyExpense(models.Model):        # change expense-hallbudget relation to aggregation
#     name = models.CharField(max_length = 100)
#     cost = models.FloatField()
#     hallbudget = models.ForeignKey(HallBudget, on_delete=models.CASCADE, related_name = "pettyexpenses") 
#     def __str__(self):
#         return self.name
   
#     def change_value(self, value):
#         self.cost = value
#         self.save()
        


# class Allocation(models.Model):     # change allocation-hallbudget relation to aggregation
#     hall_budget= models.ForeignKey(HallBudget, on_delete = models.CASCADE, related_name = "allocations")
#     name = models.CharField(max_length = 100)
#     allocated_grant = models.FloatField()

#     def __str__(self):
#         return self.name
    
#     def change_value(self, value):
#         self.allocated_grant = value
#         self.save()

# class Leave(models.Model):
#     hall= models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "leaves")
#     person= models.ForeignKey(Person, on_delete = models.CASCADE, related_name = "leaves")
#     approved = models.BooleanField(default = False)
#     description = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField()