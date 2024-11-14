from modeltranslation.translator import translator, TranslationOptions
from .models import Order, Cart
# for Person model
class OrderTranslationOptions(TranslationOptions):
    fields = ('status', )


class CartTranslationOptions(TranslationOptions):
    fields = ('status', )


translator.register(Order, OrderTranslationOptions)
translator.register(Cart, CartTranslationOptions)
