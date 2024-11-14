from django.contrib import admin
from .models import (Product, ProductImages, Brand, Review, FLAG_CHOICES)
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext as _


class ProductImagesInline(admin.TabularInline):
    model = ProductImages


class ProductAdmin(TranslationAdmin):
    inlines = [ProductImagesInline]
    search_fields = ['name']
    list_display = ['name', 'id', 'flag', 'brand']


class BrandAdmin(TranslationAdmin):
    list_display = ['name']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Review)
