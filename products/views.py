from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import (Product, Brand, Review, ProductImages)


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

