from django.db import models

from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    shop_name = models.CharField(_('Shop Name'), max_length=50)
    city = models.CharField(_('City'), max_length=255)
    street = models.CharField(_('Street'), max_length=255)
    phone_number = models.CharField(max_length=12)
    products = models.ManyToManyField('Product', blank=True)

    def __str__(self) -> str:
        return f"{self.shop_name}"
