from django.urls import path

from .views import (ProductListView, ProductDetailView, BrandListView,
                    BrandDetailView, add_review, test_celery)
from .api import (ProductListAPI, ProductDetailAPI, BrandListAPI, BrandDetailAPI)


urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brand-detail/<slug:slug>', BrandDetailView.as_view(), name='brand-detail'),
    path('', ProductListView.as_view(), name='product-list'),
    path('test_celery', test_celery, name='test-celery'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('<slug:slug>/add-review', add_review, name='add-review'),

    # API URLs
    path('api/list', ProductListAPI.as_view(), name='product-list-api'),
    path('api/list/<int:pk>', ProductDetailAPI.as_view(), name='product-detail-api'),
    path('api/brands', BrandListAPI.as_view(), name='brand-list-api'),
    path('api/brands/<int:pk>', BrandDetailAPI.as_view(), name='brand-detail-api'),

]
