from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, MessAccount

@receiver(post_save, sender=Student)
def create_mess_account(sender, instance, created, **kwargs):
    if created:
        MessAccount.objects.create(student = instance)