from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Student, MessAccount, Hall, BoarderRoom, Passbook, AmenityRoom, ComplaintRegister, HallPassbook

@receiver(post_save, sender=Student)
def create_mess_account(sender, instance, created, **kwargs):
    if created:
        MessAccount.objects.create(student = instance)

@receiver(post_save, sender=Hall)
def create_complaint_register(sender, instance, created, **kwargs):
    if created:
        ComplaintRegister.objects.create(hall = instance)
        
@receiver(post_save, sender=Hall)
def create_hallpassbook(sender, instance, created, **kwargs):
    if created:
        HallPassbook.objects.create(hall = instance)
        
@receiver(post_save, sender=Student)
def create_passbook(sender, instance, created, **kwargs):
    if created:
        Passbook.objects.create(student = instance)
        
@receiver(pre_save, sender = Hall)
def update_total_rooms(sender, instance, **kwargs):
    if instance.total_boarderrooms is not instance.boarderRooms.count():
        instance.total_boarderrooms = instance.boarderRooms.count()
        instance.save()
    
    if instance.total_amenityrooms is not instance.amenityRooms.count():
        instance.total_amenityrooms = instance.amenityRooms.count()
        instance.save()
    
@receiver(post_save, sender = BoarderRoom)
def update_current_occupancy(sender, instance, created, **kwargs):
    if instance.currentOccupancy is not instance.students.count():
        instance.currentOccupancy = instance.students.count()
        instance.save()

    instance.hall.save()
    
@receiver(post_save, sender = AmenityRoom)
def update_current_occupancy(sender, instance, created, **kwargs):
    instance.hall.save()
    
@receiver(post_save, sender = Student)
def update_sender_room_occupancy(sender, instance, **kwargs):
    if instance.room is not None:
        instance.room.save()
        
@receiver(post_delete, sender = Student)
def update_sender_room_occupancy(sender, instance, **kwargs):
    rooms = BoarderRoom.objects.all()
    for room in rooms:
        room.save()
        
@receiver(post_delete, sender = BoarderRoom)
def update_sender_room_occupancy(sender, instance, **kwargs):
    halls = Hall.objects.all()
    for hall in halls:
        hall.save()