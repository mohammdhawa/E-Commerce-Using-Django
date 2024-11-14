from django.db import models
from django.utils.translation import gettext_lazy as _


class Settings(models.Model):
    name = models.CharField(_('name'), max_length=100)
    logo = models.ImageField(_('logo'), upload_to="settings")
    subtitle = models.TextField(_('subtitle'), max_length=500)
    call_us = models.CharField(_('call us'), max_length=25)
    email_us = models.CharField(_('email us'), max_length=25)
    phones = models.TextField(_('phone'), max_length=50)
    emails = models.TextField(_('email'), max_length=50)
    address = models.TextField(_('address'), max_length=100)
    android_app = models.URLField(_('android app'), max_length=200, null=True, blank=True)
    ios_app = models.URLField(_('ios app'), max_length=200, null=True, blank=True)
    facebook = models.URLField(_('facebook'), max_length=200, null=True, blank=True)
    youtube = models.URLField(_('youtube'), max_length=200, null=True, blank=True)
    twitter = models.URLField(_('twitter'), max_length=200, null=True, blank=True)
    instagram = models.URLField(_('instagram'), max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('settings')
        verbose_name_plural = _('settings')


class DeliveryFee(models.Model):
    fee = models.FloatField(_('fee'))

    def __str__(self):
        return str(self.fee)

    class Meta:
        verbose_name = _('delivery fee')
        verbose_name_plural = _('delivery fee')
