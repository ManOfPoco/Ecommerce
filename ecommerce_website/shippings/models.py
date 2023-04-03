from django.db import models

from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


class Shipping(models.Model):
    shipping_name = models.CharField(_('Shipping Name'), max_length=255)
    shipping_type = models.ForeignKey(
        'ShippingType', on_delete=models.CASCADE, related_name='shipping')
    shipping_charge = models.IntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_shipping')
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='updated_shipping')
    estimated_days = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.shipping_name}"


class ShippingType(models.Model):
    type_name = models.CharField(_('Type name'), max_length=50)
    type_description = models.TextField(_('Type Description'))

    def __str__(self) -> str:
        return f"{self.type_name}"
