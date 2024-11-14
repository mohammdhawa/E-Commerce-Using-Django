from django.db import models
from django.contrib.auth.models import User
from utils.generate_code import user_activation_code

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('profile'), related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_('image'), default='profile/default.jpg', upload_to='profile', max_length=250)
    code = models.CharField(_('code'), max_length=10, default=user_activation_code)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


ADDRESS_CHOICES = (
    ('Home', _('Home')),
    ('Office', _('Office')),
    ('Work', _('Work')),
    ('Other', _('Other')),
)

class Address(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='user_address', on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_('type'), max_length=10, choices=ADDRESS_CHOICES)
    address = models.CharField(_('address'), max_length=200)
    default = models.BooleanField(_('default'), default=False)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')


PHONE_CHOICES = (
    ('Primary', _('Primary')),
    ('Secondary', _('Secondary')),
)

class Phone(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='user_phone', on_delete=models.CASCADE)
    type = models.CharField(_('type'), max_length=10, choices=PHONE_CHOICES)
    number = models.CharField(_('number'), max_length=25)

    class Meta:
        verbose_name = _('phone')
        verbose_name_plural = _('phones')
