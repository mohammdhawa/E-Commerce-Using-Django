from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from utils.generate_code import generate_code
from django.utils import timezone
from accounts.models import Address


ORDER_STATUS_CHOICES = (
    ('Recieved', 'Recieved'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
)
class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_owner', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)
    code = models.CharField(max_length=10, default=generate_code)
    order_time = models.DateTimeField(default=timezone.now)
    delivery_time = models.DateTimeField(null=True, blank=True)
    delivery_address = models.ForeignKey(Address, related_name='delivery_address', on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey('Coupon', related_name='order_coupon', on_delete=models.SET_NULL,
                               null=True, blank=True)
    total = models.FloatField()
    total_with_coupon = models.FloatField(null=True, blank=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_detail_product', on_delete=models.SET_NULL,
                                null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    total = models.FloatField(null=True, blank=True)


CART_STATUS_CHOICES = (
    ('Inprogress', 'Inprogress'),
    ('Completed', 'Completed'),
)
class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart_owner', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=CART_STATUS_CHOICES, default='Inprogress')
    coupon = models.ForeignKey('Coupon', related_name='cart_coupon', on_delete=models.SET_NULL,
                               null=True, blank=True)
    total_with_coupon = models.FloatField(null=True, blank=True)


class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_detail_product', on_delete=models.SET_NULL,
                                null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total = models.FloatField(null=True, blank=True)


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    quantity = models.PositiveIntegerField()
    discount = models.FloatField()

    def save(self, *args, **kwargs):
        if self.end_date is None:
            week = self.start_date + timezone.timedelta(days=7)
            self.end_date = week
        super(Coupon, self).save(*args, **kwargs)
