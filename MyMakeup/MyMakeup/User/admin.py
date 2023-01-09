from django.contrib import admin
from .models import Address

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address","landmark","state","pin")

admin.site.register(Address, AddressAdmin)