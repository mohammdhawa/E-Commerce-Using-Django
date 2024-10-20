from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


FLAG_CHOICES = (
    ('New', 'New'),
    ('Feature', 'Feature'),
    ('Sale', 'Sale'),
)

class Product(models.Model):
    name = models.CharField(_('name'), max_length=100)
    flag = models.CharField(_('flag'), max_length=10, choices=FLAG_CHOICES)
    price = models.FloatField(_('price'))
    image = models.ImageField(_('image'), upload_to='products/')
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    sku = models.CharField(_('sku'), max_length=10)
    subtitle = models.TextField(_('subtitle'), max_length=500)
    description = models.TextField(_('description'), max_length=50000)
    tags = TaggableManager()
    brand = models.ForeignKey('Brand', verbose_name=_('brand'), related_name='product_brand', on_delete=models.SET_NULL, blank=True, null=True)
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

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-id']

    @property
    def avg_rate(self):
        reviews = self.review_product.all()
        total_reviews = len(reviews)

        return 0 if total_reviews == 0 else round(sum(review.rate for review in reviews) / total_reviews, 1)

    @property
    def reviews_count(self):
        reviews = self.review_product.all().count()
        return reviews


class ProductImages(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to='products/')

    def __str__(self):
        return str(self.product)


class Brand(models.Model):
    name = models.CharField(_('name'), max_length=100)
    image = models.ImageField(_('image'), upload_to='brands/')
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
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='review_user', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='review_product', on_delete=models.CASCADE)
    review = models.TextField(_('review'), max_length=5000)
    rate = models.IntegerField(_('rate'), choices=[(i, i) for i in range(1, 6)])
    review_date = models.DateTimeField(_('review date'), default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.product}"
