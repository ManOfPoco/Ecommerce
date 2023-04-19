from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    fields = ['shop_name', 'city', 'street', 'phone_number', 'products']
    list_display = ['shop_name', 'city', 'phone_number']
    filter_horizontal = ['products']
