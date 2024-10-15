from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Brand, Review


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class BrandListView(ListView):
    model = Brand


class BrandDetailView(DetailView):
    model = Brand
