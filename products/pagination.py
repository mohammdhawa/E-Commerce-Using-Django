from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 48
    page_size_query_param = 'page_size'


class BrandPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'