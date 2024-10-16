from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Brand
from .serializers import (ProductSerializer, ProductDetailSerializer, BrandListSerializer,
                          BrandDetailSerializer)
from .pagination import ProductPagination, BrandPagination


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flag', 'brand']


class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class BrandListAPI(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    pagination_class = BrandPagination


class BrandDetailAPI(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer
