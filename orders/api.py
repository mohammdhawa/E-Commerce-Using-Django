from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.utils import timezone

from django.contrib.auth.models import User

from .serializers import (OrderSerializer, OrderDetailSerializer, CartSerializer,
                          CartDetailSerializer)
from .models import Order, OrderDetail, Cart, CartDetail, Coupon
from products.models import Product
from settings.models import DeliveryFee


class OrderListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        queryset = super(OrderListAPI, self).get_queryset()
        user = User.objects.get(username=self.kwargs['username'])
        queryset = queryset.filter(user=user)
        data = OrderSerializer(queryset, many=True).data
        return Response({'orders': data})


class OrderDetailAPI(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ApplyCouponAPI(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(user=self.kwargs['username']) # get username from url
        coupon = get_object_or_404(Coupon, code=request.data['coupon_code']) # get coupon code from request body
        cart = Cart.objects.get(user=user, status='Inprogress')
        cart_detail = CartDetail.objects.get(cart=cart)
        delivery_fee = DeliveryFee.objects.last().fee

        subtotal = cart.cart_total

        time_now = timezone.now()
        if coupon.start_date <= time_now <= coupon.end_date and coupon.quantity > 0:
            discount = round((coupon.discount / 100) * subtotal, 2)
            total = round((subtotal - discount) + delivery_fee, 2)
            cart.coupon = coupon
            cart.total_with_coupon = total
            cart.save()

            coupon.quantity -= 1
            coupon.save()

            return Response({"message": "Coupon applied successfully!"})
        else:
            return Response({"message": "Coupon is not valid or expired..."})

        return Response({"message": "Coupon not found"})
