from django.contrib import admin
from .models import WishList, WishListItem


class WishListItemInline(admin.StackedInline):
    model = WishListItem
    extra = 3


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    fields = ['user', 'list_name', 'is_default']
    inlines = [WishListItemInline]
