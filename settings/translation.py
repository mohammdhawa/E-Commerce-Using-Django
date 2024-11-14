from modeltranslation.translator import translator, TranslationOptions
from .models import Settings
# for Person model
class SettingsTranslationOptions(TranslationOptions):
    fields = ('subtitle', )


translator.register(Settings, SettingsTranslationOptions)
