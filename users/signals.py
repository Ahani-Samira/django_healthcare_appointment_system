from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import CustomUser, Doctor, Patient

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_doctor:
            Doctor.objects.create(user=instance)
        else:
            Patient.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'doctor'):
        instance.doctor.save()
    if hasattr(instance, 'patient'):
        instance.patient.save()
