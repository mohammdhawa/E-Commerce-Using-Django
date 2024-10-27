from django.shortcuts import render, redirect
from django.utils import timezone

from products.models import Product
from .models import (Order, OrderDetail, Cart, CartDetail, Coupon)
from settings.models import DeliveryFee


def order_list(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders/order_list.html', {'orders': orders})


def checkout(request):
    cart = Cart.objects.get(user=request.user, status='Inprogress')
    cart_detail = CartDetail.objects.filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee

    subtotal = cart.cart_total
    discount = 0
    total = subtotal + delivery_fee
    error = False

    if request.method == 'POST':
        coupon_code = request.POST['coupon']
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            time_now = timezone.now()
            if coupon.start_date <= time_now <= coupon.end_date and coupon.quantity > 0:
                discount = round((coupon.discount / 100) * subtotal, 2)
                total = round((subtotal - discount) + delivery_fee, 2)
                cart.coupon = coupon
                cart.total_with_coupon = total
                cart.save()
            else:
                error = True
        except Coupon.DoesNotExist:
            error = True

    context = {
        'cart': cart,
        'cart_detail': cart_detail,
        'delivery_fee': delivery_fee,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'error': error
    }


    return render(request, 'orders/checkout.html', context)


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

