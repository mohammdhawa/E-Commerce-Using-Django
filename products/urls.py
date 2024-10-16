from django.urls import path

from .views import (ProductListView, ProductDetailView, BrandListView, BrandDetailView)
from .api import ProductListAPI


urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brand-detail/<slug:slug>', BrandDetailView.as_view(), name='brand-detail'),
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product-detail'),

    # API URLs
    path('api/list', ProductListAPI.as_view(), name='product-list-api'),

]
