from django.urls import path
from .views import (OrderList, checkout, add_to_cart, process_payment,
                    payment_success, payment_failure, delete_from_cart)
from .api import OrderListAPI, OrderDetailAPI, ApplyCouponAPI, CreateOrderAPI, CartCreateUpdateDeleteAPI

urlpatterns = [
    path('', OrderList.as_view(), name='order_list'),
    path('checkout', checkout, name='checkout'),
    path('add-to-cart', add_to_cart, name='add-to-cart'),
    path('checkout/process-payment', process_payment, name='process_payment'),
    path('checkout/payment/success', payment_success, name='payment_success'),
    path('checkout/payment/failure', payment_failure, name='payment_failure'),
    path('delete_from_cart/<int:pk>', delete_from_cart, name='delete_from_cart'),

    ## API urls
    path('api/<str:username>/orders', OrderListAPI.as_view(), name="order-list-api"),
    path('api/<str:username>/orders/<int:pk>', OrderDetailAPI.as_view(), name="order-detail-api"),
    path('api/<str:username>/apply-coupon', ApplyCouponAPI.as_view(), name="apply-coupon-api"),
    path('api/<str:username>/cart', CartCreateUpdateDeleteAPI.as_view(), name="cart-create-update-delete-api"),
    path('api/<str:username>/orders/create', CreateOrderAPI.as_view(), name="order-create-api"),
]
