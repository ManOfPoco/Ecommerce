from django.db import models

from django.contrib.auth.models import User
from products.models import Product

from django.utils.translation import gettext_lazy as _


class WishList(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='wishlist')
    list_name = models.CharField(_('List Name'), max_length=100)

    def __str__(self) -> str:
        return f"{self.list_name}"


class WishListItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='wishlist_item')
    wishlist = models.ForeignKey(
        WishList, on_delete=models.CASCADE, related_name='wishlist_item')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product.product_name}"
