from django.db import models, IntegrityError
from django.db.models import Prefetch, UniqueConstraint, Sum, F, Subquery, DecimalField
from django.db.models.functions import Coalesce, Cast

from django.contrib.auth.models import User
from products.models import Product, ProductImages, ProductDiscount
from ecommerce.models import Shop

from django.core.validators import MinValueValidator

from django.utils.translation import gettext_lazy as _


class CartManager(models.Manager):

    def get_or_create_cart(self, request):
        try:
            cart = Cart.objects.get(user_id=request.user.id)

            return cart
        except Cart.DoesNotExist:
            cart = request.session.get('cart_id', None)

            if cart is None:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.pk

                return cart

            cart = Cart.objects.get(cart=cart)
            return cart


class CartItemManager(models.Manager):

    def get_cart_products(self, cart: 'Cart'):
        queryset = CartItem.objects.filter(cart=cart).select_related('product', 'pickup_shop').only(
            'product__id', 'product__product_name', 'product__slug', 'product__brand', 'product__quantity', 'product__regular_price', 'pickup_shop__shop_name'
        ).prefetch_related(Prefetch('product__images', to_attr='product_image',
                                    queryset=ProductImages.objects.filter(is_default=True))).annotate(
            current_price=Coalesce(
                Subquery(ProductDiscount.objects.get_best_discount_price()),
                F('product__regular_price')) * F('quantity'),
            base_price=F('product__regular_price') * F('quantity')
        ).order_by('-product__product_name')

        return queryset

    def check_availability(self, queryset, cart_item_instance):
        not_available_products = []
        for item in queryset:
            if item.quantity > item.product.quantity or \
                    item.product.is_active == False:
                queryset = queryset.exclude(product=item.product)
                not_available_products.append((item.product, item.cart))
                item.delete()

        for product, cart in not_available_products:
            try:
                SaveForLater.objects.create(product=product, cart=cart)
            except IntegrityError:
                continue

        if not getattr(cart_item_instance, 'not_available_products', None):
            setattr(cart_item_instance, 'not_available_products',
                    [product[0] for product in not_available_products])

        return queryset

    def calculate_bill(self, queryset):

        bill = queryset.aggregate(
            discount_price=Cast(Sum('current_price'), output_field=DecimalField(
                max_digits=10, decimal_places=2)),
            base_price=Cast(Sum('base_price'), output_field=DecimalField(max_digits=10, decimal_places=2)))

        if bill['discount_price'] != bill['base_price']:
            bill['discount_amount'] = bill['base_price'] - \
                bill['discount_price']
            # modify total_price in the future. Add order price
            bill['total_price'] = bill['discount_price']
        else:
            bill['total_price'] = bill['base_price']

        return {key: round(value, 2) for key, value in bill.items()}

    def get_cart_items_count(self, request):
        cart = Cart.objects.get_or_create_cart(request=request)
        cart_items_count = self.model.objects.filter(cart=cart).count()

        return cart_items_count


class SaveForLaterManager(models.Manager):

    def get_cart_products(self, cart: 'Cart'):
        queryset = SaveForLater.objects.filter(cart=cart).select_related('product').only(
            'product__product_name', 'product__slug', 'product__brand', 'product__quantity', 'product__regular_price'
        ).prefetch_related(Prefetch('product__discounts', to_attr='product_discounts'),
                           Prefetch('product__images', to_attr='product_image', queryset=ProductImages.objects.filter(is_default=True)))

        return queryset


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart', blank=True, null=True)

    objects = CartManager()

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
