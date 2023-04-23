from django.db import models

from django.contrib.auth.models import User
from products.models import Product
from shippings.models import Shipping

from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='order')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.OneToOneField(Shipping, on_delete=models.CASCADE)
    order_status = models.ForeignKey(
        'OrderStatus', on_delete=models.CASCADE, related_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    order_delivery_date = models.DateTimeField(auto_now=True)
    shipping_history = models.JSONField(default=list)
    status_history = models.JSONField(default=list)

    def __str__(self) -> str:
        return f"{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='order_item')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.product.product_name}"


class OrderStatus(models.Model):
    status_name = models.CharField(_('Status Name'), max_length=100)

    class Meta:
        verbose_name_plural = 'Order Statuses'

    def __str__(self) -> str:
        return f"{self.status_name}"
