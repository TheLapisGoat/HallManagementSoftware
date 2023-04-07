from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Student, MessAccount, Hall, BoarderRoom, AmenityRoom

@receiver(post_save, sender=Student)
def create_mess_account(sender, instance, created, **kwargs):
    if created:
        MessAccount.objects.create(student = instance)
        
@receiver(post_save, sender = Hall)
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