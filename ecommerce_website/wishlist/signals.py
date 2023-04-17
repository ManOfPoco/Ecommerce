from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import WishList

from django.template.defaultfilters import slugify


@receiver(post_save, sender=WishList)
def wishlist_slug_creation(sender, instance, created, **kwargs):
    if created:
        instance.slug = slugify(instance.list_name)
        instance.save()
