from rest_framework import generics, status
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

            return Response({"message": "Coupon applied successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Coupon is not valid or expired..."})

        return Response({"message": "Coupon not found"}, status=status.HTTP_404_NOT_FOUND)


class CreateOrderAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(user=self.kwargs['username'])
        code = request.data['coupon_code']
        delivery_address = request.data['address_id']

        cart = Cart.objects.get(user=user, status='Inprogress')
        cart_detail = CartDetail.objects.filter(cart=cart)
        user_address = Address.objects.get(id=delivery_address)

        # Cart: Order | Cart Detail : Order Detail
        new_order = Order.objects.create(
            user=user,
            status='Recieved',
            delivery_address=user_address,
            coupon=cart.coupon,
            total_with_coupon=cart.total_with_coupon,
            total=cart.cart_total
        )

        # Order Detail
        for item in cart_detail:
            product = Product.objects.get(id=item.product.id)
            OrderDetail.objects.create(
                order=new_order,
                product=product,
                quantity=item.quantity,
                price=item.product.price,
                total=round(item.quantity * product.price, 2)
            )

            # Decrease product quantity
            product.quantity -= item.quantity
            product.save()

        # Close cart
        cart.status = "Completed"
        cart.save()

        # send email to user
        return Response({"message": "Order created successfully!"}, status=status.HTTP_200_OK)


class CartCreateUpdateDeleteAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass