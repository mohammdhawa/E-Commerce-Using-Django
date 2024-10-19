from django.shortcuts import render

from products.models import Brand, Product, Review


def home(request):
    brands = Brand.objects.all().order_by('-id')[:10]
    feature_products = Product.objects.filter(flag='Feature')[:6]
    sale_products = Product.objects.filter(flag='Sale')[:10]
    new_products = Product.objects.filter(flag='New')[:6]
    reviews = Review.objects.order_by('rate')[:4]

    context = {'brands': brands, 'feature_products': feature_products,
               'sale_products': sale_products, 'reviews': reviews,
               'new_products': new_products}
    return render(request, 'settings/home.html', context)
