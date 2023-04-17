from django.apps import AppConfig


class WishlistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wishlist'

    def ready(self) -> None:
        from . import signals
        return super().ready()
