from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver 
from .models import Employee

@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        # Every new User gets a 'Shadow' Employee profile.
        Employee.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_employee_profile(sender, instance, **kwargs):
    # This ensures that if the User is updated, the Employee profile is also saved
    if hasattr(instance, 'employee'):
        instance.employee.save()