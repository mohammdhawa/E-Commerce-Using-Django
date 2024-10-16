from rest_framework import serializers
from .models import (Product, ProductImages, Brand, Review)


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = ['user', 'product', 'review', 'rate', 'review_date']


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    product_image = ProductImagesSerializer(many=True)
    review_product = ReviewSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
