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
    review_count = serializers.SerializerMethodField()
    avg_review = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_review_count(self, object):
        count = Review.objects.filter(product=object).count()
        return count

    def get_avg_review(self, object):
        sum = 0
        reviews = Review.objects.filter(product=object)

        for review in reviews:
            sum += review.rate

        if len(reviews) == 0:
            return 0

        return round(sum / len(reviews), 1)


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    product_image = ProductImagesSerializer(many=True)
    review_product = ReviewSerializer(many=True)
    review_count = serializers.SerializerMethodField()
    avg_review = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_review_count(self, object):
        count = Review.objects.filter(product=object).count()
        return count

    def get_avg_review(self, object):
        sum = 0
        reviews = Review.objects.filter(product=object)

        for review in reviews:
            sum += review.rate

        return round(sum / len(reviews), 1)


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
