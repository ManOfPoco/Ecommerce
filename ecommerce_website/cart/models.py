from django.db import models
from django.db.models import Prefetch, UniqueConstraint, Sum, F, OuterRef, Subquery, Q
from django.db.models.functions import Coalesce

from django.contrib.auth.models import User
from products.models import Product, ProductImages, ProductDiscount
from ecommerce.models import Shop

from django.core.validators import MinValueValidator

from django.utils.translation import gettext_lazy as _


class CartItemManager(models.Manager):

    def get_cart_products(self, cart: 'Cart'):
        queryset = CartItem.objects.filter(cart=cart).select_related('product', 'pickup_shop').only(
            'product__product_name', 'product__slug', 'product__brand', 'product__quantity', 'product__regular_price', 'pickup_shop__shop_name'
        ).prefetch_related(Prefetch('product__discounts', to_attr='product_discounts'),
                           Prefetch('product__images', to_attr='product_image',
                                    queryset=ProductImages.objects.filter(is_default=True)))

        return queryset

    def calculate_bill(self, cart_items):
        discounts = ProductDiscount.objects.filter(
            Q(product=OuterRef('product')) &
            Q(minimum_order_value__lte=OuterRef('quantity')) &
            Q(maximum_order_value__gte=OuterRef('quantity'))
        ).order_by("-discount_unit").values('discount_price')

        queryset = cart_items.annotate(
            current_price=Coalesce(
                Subquery(discounts[:1]), F('product__regular_price')
            ) * F('quantity')
        )

        bill = queryset.aggregate(
            bill=Sum('current_price'))['bill']
        return bill


class SaveForLaterManager(models.Manager):

    def get_cart_products(self, cart: 'Cart'):
        queryset = SaveForLater.objects.filter(cart=cart).select_related('product').only(
            'product__product_name', 'product__slug', 'product__brand', 'product__quantity', 'product__regular_price'
        ).prefetch_related(Prefetch('product__discounts', to_attr='product_discounts'),
                           Prefetch('product__images', to_attr='product_image', queryset=ProductImages.objects.filter(is_default=True)))

        return queryset


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        verbose_name_plural = 'Carts'

    def __str__(self) -> str:
        return f"Cart - {self.user}"


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    pickup_shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name='cart_item', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = CartItemManager()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['product', 'cart'], name='unique_product_in_cart',
                             violation_error_message="Cart can't have the same products")
        ]

    def __str__(self) -> str:
        return f"{self.product.product_name}"


class SaveForLater(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='save_for_later')
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='save_for_later')

    objects = SaveForLaterManager()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['product', 'cart'], name='unique_product_in_save_for_later',
                             violation_error_message="Save For Later can't have the same products")
        ]
