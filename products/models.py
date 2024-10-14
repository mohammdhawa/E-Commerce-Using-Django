from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone


FLAG_CHOICES = (
    ('New', 'New'),
    ('Feature', 'Feature'),
    ('Sale', 'Sale'),
)

class Product(models.Model):
    name = models.CharField(max_length=100)
    flag = models.CharField(max_length=10, choices=FLAG_CHOICES)
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')
    quantity = models.PositiveIntegerField(default=1)
    sku = models.CharField(max_length=10)
    subtitle = models.TextField(max_length=500)
    description = models.TextField(max_length=50000)
    tags = TaggableManager()
    brand = models.ForeignKey('Brand', related_name='product_brand', on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # check for uniqueness
            original_slug = self.slug
            queryset = Product.objects.filter(slug=original_slug)
            count = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{count}"
                count += 1
                queryset = Product.objects.filter(slug=self.slug)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return str(self.product)


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brands/')
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # check for uniqueness
            original_slug = self.slug
            queryset = Brand.objects.filter(slug=original_slug)
            count = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{count}"
                count += 1
                queryset = Brand.objects.filter(slug=self.slug)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, related_name='review_user', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='review_product', on_delete=models.CASCADE)
    review = models.TextField(max_length=5000)
    rate = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_date = models.DateTimeField(default=timezone.now)
