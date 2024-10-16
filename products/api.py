from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Product, Brand
from .serializers import (ProductSerializer, ProductDetailSerializer, BrandListSerializer,
                          BrandDetailSerializer)


class ProductPagination(PageNumberPagination):
    page_size = 48
    page_size_query_param = 'page_size'


class BrandPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


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
