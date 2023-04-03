from django.db import models

from products.models import Product

from django.core.validators import MinValueValidator


class Sells(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='sells')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name_plural = 'Sells'

    def __str__(self) -> str:
        return f"{self.product} with total pirce = {self.total_price}"
