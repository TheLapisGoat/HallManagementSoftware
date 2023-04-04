from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
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
        ('admission', 'AdmissionUnit')
    ]
    
    role = models.CharField("Role", max_length=40, choices=ROLES, default='student')

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"
        
    address = models.TextField("Address")
    telephoneNumber = models.IntegerField("TelephoneNumber")
    #photograph = models.ImageField("Photo")

    REQUIRED_FIELDS = ["email", "address", "telephoneNumber", "role", "first_name", "last_name"]

class Hall(models.Model):
    name = models.CharField("Name", max_length = 100, blank = False, primary_key = True)
    total_rooms  = models.IntegerField("Total Rooms", default = 0)
    
    def save(self, *args, **kwargs):
        self.total_rooms = self.boarderRooms.count()
        super(Hall, self).save(*args, **kwargs)
        
    def getCurrentOccupancy(self):
        return self.boarderRooms.aggregate(total = Sum('currentOccupancy'))['total']
    
    def getMaxOccupancy(self):
        return self.boarderRooms.aggregate(total = Sum('maxOccupancy'))['total']
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(Hall, self).save(*args, **kwargs)
            self.total_rooms = self.boarderRooms.count()
            self.save()
        else:
            self.total_rooms = self.boarderRooms.count()
            super(Hall, self).save(*args, **kwargs)
        
    #messManager = models.OneToOneField(MessManager, on_delete = models.CASCADE, related_name = "messManager")
    #not in the class diagram and changed it locally
    # warden = models.OneToOneField(Warden, on_delete = models.CASCADE, related_name = "warden")
    # expenditure = models.OneToOneField(HallBudget, on_delete = models.CASCADE, related_name = "expenditure")

class Room(models.Model):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "rooms", blank = False)
    roomNumber = models.CharField("Room Number", max_length = 100, blank = False)
    rent = models.FloatField("Rent", default = 0, blank = False)
    
    def __str__(self):
        return self.roomNumber
    def getRent(self):
        return self.rent
    def getRoomNumber(self):
        return self.roomNumber
    
    class Meta:
        abstract = True
        

# class AmenityRoom(Room):
#     hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "amenityRooms")
#     amenityName = models.CharField(max_length = 100)

#     def getAmenityName(self):
#         return self.amenityName

class BoarderRoom(Room):
    hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "boarderRooms", blank = False)
    newstatus = models.BooleanField("New Status", blank = False, default = True)
    maxOccupancy = models.IntegerField("Max Occupancy", blank = False)
    currentOccupancy = models.IntegerField("Current Occupancy", blank = False, default = 0)

    def getNewStatus(self):
        return self.newstatus
    def getOccupancyNumber(self):
        return self.occupancyNumber
    def setOccupancyNumber(self, value):
        self.occupancyNumber = value
        self.save()
    def getCurrentNoStudents(self):
        return self.currentnoStudents
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(BoarderRoom, self).save(*args, **kwargs)
            self.currentOccupancy = self.students.count()
            self.save()
            self.hall.save()
        else:
            self.currentOccupancy = self.students.count()
            super(BoarderRoom, self).save(*args, **kwargs)
            self.hall.save()
        
    
class Student(models.Model):
    person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "student", primary_key = True, blank = False)
    hall = models.ForeignKey(Hall, on_delete = models.PROTECT, related_name = "students", blank = False)
    rollNumber = models.CharField("Roll Number", max_length = 100, blank = False)
    room = models.ForeignKey(BoarderRoom, on_delete = models.PROTECT, related_name = "students", blank = False) 
    # def getHall(self):
        # return self.hall
    def getRollNumber(self):
        return self.rollNumber
    # def getRoomNumber(self):
    #     return self.room.getRoomNumber()
    # def getMessDue(self):
    #     return self.messAccount.getDue()
    # def getRoomRent(self):
    #     return self.room.getRent()
    # def getAmenityDues(self):
    # return self.hall.amenityRoom.getRent()
    #roomNumber = models.ForeignKey()
    
    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)
        self.room.save()

# class Warden(models.Model):
#     person = models.OneToOneField(Person, on_delete = models.CASCADE, related_name = "warden", primary_key = True)
#     #IAMAWARDEN

# class Fees(models.Model):
#     student = models.OneToOneField(Student, on_delete = models.CASCADE, related_name = "fees")
#     amenityFees = models.FloatField()
#     roomFees = models.FloatField()
#     def getAmenityFees(self):
#         return self.amenityFees
#     def getRoomFees(self):
#         return self.roomFees

# class MessAccount(models.Model):
#     student = models.OneToOneField(Student, on_delete = models.CASCADE, related_name = "messAccount")
#     due = models.FloatField()
    
#     def getDue(self):
#         return self.due
#     def setDue(self, value):
#         self.due = value
#         self.save()
            
# class ComplaintRegister(models.Model):
#     hall = models.ForeignKey(Hall, on_delete = models.CASCADE, related_name = "complaintRegister")
    
    
# class Complaint(models.Model):
#     ComplaintRegister = models.ForeignKey(ComplaintRegister, on_delete = models.CASCADE, related_name = "complaints")
#     details = models.TextField()
#     date = models.DateField()
#     nameagainst = models.CharField(max_length = 100)
#     #image = models.ImageField()
#     status = models.CharField(max_length = 100)

# class ATR(models.Model):
#     name = models.CharField(max_length = 100)
#     details = models.TextField()
#     complaint = models.ForeignKey(Complaint, on_delete = models.CASCADE, related_name = "ATR")

#     def change_status(self, status):
#         self.status = status
#         self.save()

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