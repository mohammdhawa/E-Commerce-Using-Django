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
        fields = ['name', 'flag', 'price', 'image', 'quantity', 'sku',
                  'subtitle', 'description', 'brand', 'reviews_count',
                  'avg_rate']


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    images = ProductImagesSerializer(many=True, source='product_image')
    reviews = ReviewSerializer(many=True, source='review_product')
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'flag', 'price', 'image', 'quantity', 'sku',
                  'subtitle', 'description', 'brand','tags', 'reviews_count',
                  'avg_rate', 'images', 'reviews']



class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
