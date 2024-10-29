from django.urls import path
from .views import order_list, checkout, add_to_cart
from .api import OrderListAPI, OrderDetailAPI, ApplyCouponAPI, CreateOrderAPI, CartCreateUpdateDeleteAPI

urlpatterns = [
    path('', order_list, name='order_list'),
    path('checkout', checkout, name='checkout'),
    path('add-to-cart', add_to_cart, name='add-to-cart'),

    ## API urls
    path('api/<str:username>/orders', OrderListAPI.as_view(), name="order-list-api"),
    path('api/<str:username>/orders/<int:pk>', OrderDetailAPI.as_view(), name="order-detail-api"),
    path('api/<str:username>/apply-coupon', ApplyCouponAPI.as_view(), name="apply-coupon-api"),
    path('api/<str:username>/cart', CartCreateUpdateDeleteAPI.as_view(), name="cart-create-update-delete-api"),
    path('api/<str:username>/orders/create', CreateOrderAPI.as_view(), name="order-create-api"),
]
