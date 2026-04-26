from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 
    room = models.ForeignKey('properties.Room', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True) 
    start_date = models.DateField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('TENANT', 'Tenant'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='TENANT')
    room = models.ForeignKey('properties.Room', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# --- SIGNALS TO AUTO-CREATE PROFILE WHEN A USER IS CREATED ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='TENANT')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()