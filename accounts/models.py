from django.db import models
from django.contrib.auth.models import User


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
