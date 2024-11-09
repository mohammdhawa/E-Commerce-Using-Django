from itertools import product

from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from utils.generate_code import generate_code
from django.utils import timezone
from accounts.models import Address
from django.utils.translation import gettext_lazy as _


ORDER_STATUS_CHOICES = (
    ('Recieved', 'Recieved'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
)
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=_('order owner') ,related_name='order_owner', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(_('status'), max_length=10, choices=ORDER_STATUS_CHOICES)
    code = models.CharField(_('code'), max_length=10, default=generate_code)
    order_time = models.DateTimeField(_('order time'), default=timezone.now)
    delivery_time = models.DateTimeField(_('deliery time'), null=True, blank=True)
    delivery_address = models.ForeignKey(Address, verbose_name=_('delivery address'), related_name='delivery_address', on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey('Coupon', verbose_name=_('coupon'), related_name='order_coupon', on_delete=models.SET_NULL,
                               null=True, blank=True)
    total = models.FloatField(_('total'))
    total_with_coupon = models.FloatField(_('total with coupon'), null=True, blank=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'), related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='order_detail_product', on_delete=models.SET_NULL,
                                null=True, blank=True)
    quantity = models.PositiveIntegerField(_('quantity'))
    price = models.FloatField(_('price'))
    total = models.FloatField(_('total'), null=True, blank=True)


CART_STATUS_CHOICES = (
    ('Inprogress', 'Inprogress'),
    ('Completed', 'Completed'),
)
class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name=_('cart owner'), related_name='cart_owner', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(_('status'), max_length=10, choices=CART_STATUS_CHOICES)
    coupon = models.ForeignKey('Coupon', verbose_name=_('cart coupon'), related_name='cart_coupon', on_delete=models.SET_NULL,
                               null=True, blank=True)
    total = models.FloatField(_('total'), null=True, blank=True)
    total_with_coupon = models.FloatField(_('total with coupon'), null=True, blank=True)

    @property
    def cart_total(self):
        total = 0
        for item in self.cart_details.all():
            total += item.total
        return round(total, 2)


class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart details'), related_name='cart_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_('cart detail product'), related_name='cart_detail_product', on_delete=models.SET_NULL,
                                null=True, blank=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    total = models.FloatField(_('total'), null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.total:
            total = self.product.price * self.quantity
            self.total = total
        # Call the parent save method to actually save the data
        super().save(*args, **kwargs)


class Coupon(models.Model):
    code = models.CharField(_('code'), max_length=20)
    start_date = models.DateTimeField(_('start date'), default=timezone.now)
    end_date = models.DateTimeField(_('end date'), null=True, blank=True)
    quantity = models.PositiveIntegerField(_('quantity'))
    discount = models.FloatField(_('discount amount'))

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if self.end_date is None:
            week = self.start_date + timezone.timedelta(days=7)
            self.end_date = week
        super(Coupon, self).save(*args, **kwargs)
