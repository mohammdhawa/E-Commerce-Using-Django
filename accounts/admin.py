from django.contrib import admin
from .models import Address, Profile, Phone


class AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'user', 'type', 'id']


admin.site.register(Address, AddressAdmin)
admin.site.register(Profile)
admin.site.register(Phone)
