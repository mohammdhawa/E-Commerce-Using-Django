
from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Brand, Review

# for Person model
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'subtitle', 'description', 'flag')


class BrandTranslationOptions(TranslationOptions):
    fields = ('name', )


class ReviewTranslationOptions(TranslationOptions):
    fields = ('review', )


translator.register(Product, ProductTranslationOptions)
translator.register(Brand, BrandTranslationOptions)
translator.register(Review, ReviewTranslationOptions)
