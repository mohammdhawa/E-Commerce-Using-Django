from rest_framework import generics

from django.contrib.auth.models import User

from .serializers import (OrderSerializer, OrderDetailSerializer, CartSerializer,
                          CartDetailSerializer)
from .models import Order, OrderDetail, Cart, CartDetail, Coupon
from products.models import Product
from settings.models import DeliveryFee


class OrderListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = super(OrderListAPI, self).get_queryset()
        queryset = queryset.filter(user__username=self.kwargs['username'])
        return queryset
