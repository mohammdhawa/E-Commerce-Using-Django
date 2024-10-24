from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from utils.generate_code import generate_code
from django.utils import timezone


ORDER_STATUS_CHOICES = (
    ('Recieved', 'Recieved'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
)
class Order(models.Model):
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='Delivered')
    code = models.CharField(max_length=10, default=generate_code)
    order_time = models.DateTimeField(default=timezone.now)
    delivery_time = models.DateTimeField(null=True, blank=True)
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
    total = models.FloatField()


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
