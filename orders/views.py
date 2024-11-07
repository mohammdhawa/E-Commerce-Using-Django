from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings

from products.models import Product
from .models import (Order, OrderDetail, Cart, CartDetail, Coupon)
from settings.models import DeliveryFee
from utils.generate_code import generate_code
from accounts.models import Address
from django.contrib.auth.decorators import login_required

import stripe


def order_list(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders/order_list.html', {'orders': orders})


def checkout(request):
    cart = Cart.objects.get(user=request.user, status='Inprogress')
    cart_detail = CartDetail.objects.filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee

    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE

    subtotal = cart.cart_total
    discount = 0
    total = subtotal + delivery_fee
    cart.total = total
    cart.save()
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

                coupon.quantity -= 1
                coupon.save()
            else:
                error = True
                print("Error Occured in checkout function")
        except Coupon.DoesNotExist:
            error = True
            print("Error Occured in checkout function")

    context = {
        'cart': cart,
        'cart_detail': cart_detail,
        'delivery_fee': delivery_fee,
        'subtotal': subtotal,
        'discount': discount,
        'total': round(total, 2),
        'error': error,
        'pub_key': pub_key,
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

    cart = Cart.objects.get(user=request.user, status='Inprogress')
    cart_detail_data = CartDetail.objects.filter(cart=cart)

    total = cart.cart_total
    cart_count = len(cart_detail_data)

    page = render_to_string('cart_includes.html', {'cart_detail_data': cart_detail_data, 'cart_data': cart})
    return JsonResponse({'result': page, 'total': total, 'cart_count': cart_count})


@login_required
def process_payment(request): # create invoice
    print('\n\n****************************** Process Payment *************************************\n\n')
    cart = Cart.objects.get(user=request.user, status='Inprogress')
    delivery_fee = DeliveryFee.objects.last().fee

    if cart.total_with_coupon:
        total = cart.total_with_coupon + delivery_fee
    else:
        total = cart.cart_total + delivery_fee

    # Generate code to new order
    code = generate_code()
    print(f"Generated code {code}")

    # django sessions
    request.session['order_code'] = code
    request.session.save()

    # Create invoice
    stripe.api_key = settings.STRIPE_API_KEY_SECRET

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    'currency': 'usd',
                    'product_data': {'name': code},
                    'unit_amount': int(total * 100)
                },
                'quantity': 1
            },
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/orders/checkout/payment/success',
        cancel_url='http://127.0.0.1:8000/orders/checkout/payment/failure',
    )

    return JsonResponse({'session': checkout_session})


def payment_success(request): # If payment successed
    print('\n\n****************************** Payment Success *************************************\n\n')
    try:
        cart = Cart.objects.get(user=request.user, status='Inprogress')
    except Cart.DoesNotExist:
        return redirect('home')
    cart_detail = CartDetail.objects.filter(cart=cart)
    user_address = Address.objects.last()
    delivery_fee = DeliveryFee.objects.last().fee

    code = request.session.get('order_code')
    print(f"code: {code}")

    # Cart: Order | Cart Detail : Order Detail
    new_order = Order.objects.create(
        user=request.user,
        status='Recieved',
        code=code,
        delivery_address=user_address,
        coupon=cart.coupon,
        total_with_coupon= cart.total_with_coupon if cart.total_with_coupon else 0,
        total=cart.total if cart.total else 0,
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

    discount = 0
    subtotal = 0
    total = 0
    if new_order.total_with_coupon:
        discount = new_order.total - new_order.total_with_coupon
        total = new_order.total_with_coupon
        subtotal = total - delivery_fee + discount
    else:
        total = new_order.total - delivery_fee
        subtotal = total - delivery_fee

    order_details = OrderDetail.objects.filter(order=new_order)

    context = {
        'order': new_order,
        'order_details': order_details,
        'discount': round(discount, 2),
        'code': code,
        'total': round(total, 2),
        'subtotal': round(subtotal, 2),
        'delivery_fee': delivery_fee,
    }

    return render(request, 'orders/success.html', context)


def payment_failure(request): # if payment failure

    return render(request, 'orders/failure.html', {})