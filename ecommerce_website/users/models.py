from django.db import models

from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


class DeliveryAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='delivery_address')
    city = models.CharField(_('City'), max_length=255)
    street = models.CharField(_('Street'), max_length=255)
    phone_number = models.CharField(max_length=12)

    class Meta:
        verbose_name_plural = 'Delivery Addresses'

    def __str__(self) -> str:
        return f"{self.city}, {self.street}, {self.phone_number}"
