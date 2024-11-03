from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import (Product, Brand, Review, ProductImages)
from .forms import ReviewForm
from .tasks import execute_something


def test_celery(request):
    execute_something.delay()

    return render(request, 'products/test_celery.html', {})


class ProductListView(ListView):
    model = Product
    paginate_by = 48


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.get_object())
        context['images'] = ProductImages.objects.filter(product=self.get_object())
        context['related'] = Product.objects.filter(brand=self.get_object().brand)[:10]
        return context


class BrandListView(ListView):
    model = Brand
    paginate_by = 25
    queryset = Brand.objects.annotate(product_count=Count('product_brand'))


class BrandDetailView(ListView):
    model = Product
    template_name = 'products/brand_detail.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.objects.filter(slug=self.kwargs['slug']).annotate(product_count=Count('product_brand'))[0]
        context['brand'] = brand
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(brand__slug=self.kwargs['slug'])
        return queryset


def add_review(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        rate = int(request.POST.get('rate', 0))
        review_text = request.POST.get('review', '')
        Review.objects.create(user=user, product=product, rate=rate, review=review_text)

        # Get all reviews for this product after adding the new one
        reviews = Review.objects.filter(product=product)
        rendered_reviews = render_to_string('includes/reviews.html', {'reviews': reviews})
        return JsonResponse({'result': rendered_reviews})

    # Fallback if not a POST request
    return JsonResponse({'result': 'Invalid request'}, status=400)
