from django.db import models

from django.contrib.auth.models import User
from products.models import Product

from django.core.validators import MinValueValidator

from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f"{self.product.product_name}"


class SaveForLater(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='save_for_later')
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='save_for_later')
