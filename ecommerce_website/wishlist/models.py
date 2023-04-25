from django.db import models
from django.db.models import Prefetch

from django.contrib.auth.models import User
from products.models import Product, ProductImages

from django.utils.translation import gettext_lazy as _

from django.db.models import UniqueConstraint


class WishListItemsManager(models.Manager):

    def get_wishlist_products(self, wishlist, ordering='date-added'):
        queryset = WishListItem.objects.filter(
            wishlist=wishlist).select_related('product').only(
            'product__id', 'product__product_name', 'product__slug', 'product__sku', 'product__quantity', 'product__regular_price'
        ).prefetch_related(Prefetch('product__discounts', to_attr='product_discounts'),
                           Prefetch('product__images', to_attr='product_image', queryset=ProductImages.objects.filter(is_default=True)))

        wishlist_items_ordering = {
            'date-added': queryset.order_by('-date_added'),
            'name_ascending': queryset.order_by('-product__product_name'),
            'price-up': queryset.order_by('product__regular_price'),
            'price-down': queryset.order_by('-product__regular_price'),
        }

        queryset = wishlist_items_ordering.get(
            ordering, queryset.order_by('-date_added'))

        return queryset


class WishList(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='wishlist')
    list_name = models.CharField(_('List Name'), max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.list_name}"


class WishListItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='wishlist_item')
    wishlist = models.ForeignKey(
        WishList, on_delete=models.CASCADE, related_name='wishlist_item')
    date_added = models.DateTimeField(auto_now_add=True)

    objects = WishListItemsManager()

    def __str__(self) -> str:
        return f"{self.product.product_name}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['product', 'wishlist'],
                             name='unique_product_in_wishlist',
                             violation_error_message="Wishlist can't have the same products")
        ]
