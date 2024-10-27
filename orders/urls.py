from django.urls import path
from .views import order_list, checkout, add_to_cart


urlpatterns = [
    path('', order_list, name='order_list'),
    path('checkout', checkout, name='checkout'),
    path('add-to-cart', add_to_cart, name='add-to-cart'),
]
