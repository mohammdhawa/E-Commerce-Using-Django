from rest_framework import serializers
from .models import (Product, ProductImages, Brand, Review)


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = '__all__'
