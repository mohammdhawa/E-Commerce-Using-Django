from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer


class ProductPagination(PageNumberPagination):
    page_size = 48
    page_size_query_param = 'page_size'


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
