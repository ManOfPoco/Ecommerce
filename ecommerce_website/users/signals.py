from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile
from wishlist.models import WishList
from cart.models import Cart


@receiver(post_save, sender=User)
def user_dependencies_creation(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            Profile.objects.create(user=instance)
            WishList.objects.create(
                user=instance,
                list_name='default',
                slug='default',
                is_default=True)
            Cart.objects.create(user=instance)
