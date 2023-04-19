from django.contrib import admin

from .models import Cart, CartItem, SaveForLater


class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 3


class SaveForLaterInline(admin.StackedInline):
    model = SaveForLater
    extra = 3


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline, SaveForLaterInline]
