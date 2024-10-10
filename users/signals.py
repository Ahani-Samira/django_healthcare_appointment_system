from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Doctor, Patient

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_doctor:
            Doctor.objects.create(user=instance)
        else:
            Patient.objects.create(user=instance)
