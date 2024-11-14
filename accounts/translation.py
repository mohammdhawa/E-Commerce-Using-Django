from modeltranslation.translator import translator, TranslationOptions
from .models import Profile, Address, Phone


# for Person model
class AddressTranslationOptions(TranslationOptions):
    fields = ('type', )


class PhoneTranslationOptions(TranslationOptions):
    fields = ('type', )


translator.register(Address, AddressTranslationOptions)
translator.register(Phone, PhoneTranslationOptions)