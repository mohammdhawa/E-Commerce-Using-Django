from django.shortcuts import render, redirect
from redis.commands.search.reducers import quantile

from products.models import Product
from .models import (Order, OrderDetail, Cart, CartDetail, Coupon)


def order_list(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders/order_list.html', {'orders': orders})


def checkout(request):

    return render(request, 'orders/checkout.html', {})


def add_to_cart(request):
    cart = Cart.objects.get(user=request.user, status='Inprogress')
    product = Product.objects.get(id=request.POST['product_id'])

    quantity = int(request.POST['quantity'])

    if quantity > product.quantity:
        print("Error there are no such this quantity of this product")
        return

    cart_detail, created = CartDetail.objects.get_or_create(
        cart=cart,
        product=product,
    )
    cart_detail.quantity = quantity
    cart_detail.total = round(product.price * quantity, 2)
    cart_detail.save()


    return redirect("product-detail", slug=product.slug)

