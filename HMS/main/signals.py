from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Student, MessAccount, Hall, BoarderRoom, Passbook

@receiver(post_save, sender=Student)
def create_mess_account(sender, instance, created, **kwargs):
    if created:
        MessAccount.objects.create(student = instance)
        
@receiver(post_save, sender=Student)
def create_mess_account(sender, instance, created, **kwargs):
    if created:
        Passbook.objects.create(student = instance)
        
@receiver(pre_save, sender = Hall)
def update_total_rooms(sender, instance, **kwargs):
    instance.total_rooms = instance.boarderRooms.count()
    
@receiver(pre_save, sender = BoarderRoom)
def update_current_occupancy(sender, instance, **kwargs):
    instance.currentOccupancy = instance.students.count()
    instance.hall.save()
    
@receiver(post_save, sender = Student)
def update_sender_room_occupancy(sender, instance, **kwargs):
    if instance.room is not None:
        instance.room.save()