from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product, Category, Brand

from django.template.defaultfilters import slugify


@receiver(post_save, sender=Product)
def product_slug_creation(sender, instance: Product, created, **kwargs):
    if created:
        if not instance.slug:
            instance.slug = slugify(instance.product_name)
            instance.save()


@receiver(post_save, sender=Category)
def category_slug_creation(sender, instance: Category, created, **kwargs):
    if created:
        if not instance.slug:
            instance.slug = slugify(instance.category_name)
            instance.save()


@receiver(post_save, sender=Brand)
def brand_slug_creation(sender, instance: Brand, created, **kwargs):
    if created:
        if not instance.slug:
            instance.slug = slugify(instance.brand_name)
            instance.save()
