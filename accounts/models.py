from django.db import models
from django.contrib.auth.models import User
from utils.generate_code import generate_code

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(default='profile/default.jpg', upload_to='profile', max_length=250)
    code = models.CharField(max_length=10, default=generate_code)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


ADDRESS_CHOICES = (
    ('Home', 'Home'),
    ('Office', 'Office'),
    ('Work', 'Work'),
    ('Other', 'Other'),
)

class Address(models.Model):
    user = models.ForeignKey(User, related_name='user_address', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ADDRESS_CHOICES)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.address


PHONE_CHOICES = (
    ('Primary', 'Primary'),
    ('Secondary', 'Secondary'),
)

class Phone(models.Model):
    user = models.ForeignKey(User, related_name='user_phone', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=PHONE_CHOICES)
    number = models.CharField(max_length=15)
