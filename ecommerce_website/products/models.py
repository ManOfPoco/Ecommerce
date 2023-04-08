from django.db import models
from django.db.models import Prefetch, Avg, Count, Q

from mptt.models import MPTTModel, TreeForeignKey
from shippings.models import ShippingType

from django.core.validators import MinValueValidator

from django.utils.translation import gettext_lazy as _

from django.core.cache import cache
from django.http import Http404

from django.template.defaultfilters import slugify

from decimal import Decimal
from collections import defaultdict


class ProductManager(models.Manager):

    def get_popular_products(self, category=None):
        queryset = self.filter(is_active=True).select_related('brand').prefetch_related(
            Prefetch('images', queryset=ProductImages.objects.filter(is_default=True)))

        queryset = queryset.prefetch_related(Prefetch(
            'discounts', queryset=ProductDiscount.objects.order_by('discount_unit')))

        if category:
            categories = category.get_descendants(include_self=True)
            queryset = queryset.filter(category__in=categories)

        return queryset[:10]

    def get_unique_product_brands(self, category, include_count=False):
        brands = cache.get(
            f'CACHED_BRANDS_FOR_{slugify(category.category_name)}'
        )

        if brands is None:
            brands = Brand.objects.filter(
                product__category=category).distinct()

            if include_count:
                brands = brands.annotate(count=Count(
                    'product', filter=Q(product__category=category)))

            cache.set(
                f'CACHED_BRANDS_FOR_{slugify(category.category_name)}', brands, 60*60)

        return brands

    def get_products(self, category, filters=None):
        category_descendants = category.get_descendants(include_self=True)
        queryset = self.filter(
            category__in=category_descendants, is_active=True)

        if filters:
            if filters.get('price_from') and filters.get('price_to'):
                try:
                    price_from, price_to = Decimal(
                        filters['price_from']), Decimal(filters['price_to'])
                except ValueError:
                    raise Http404

                queryset = queryset.filter(
                    regular_price__range=(price_from, price_to))

                filters.pop('price_from')
                filters.pop('price_to')

            if filters.get('reviews'):
                rating = min(filters.get('reviews'))

                queryset = queryset.filter(
                    reviews__product_rating__gte=rating)
                filters.pop('reviews')

            if filters.get('brand'):
                brands = filters.get('brand')
                lookup = 'brand__brand_name' if isinstance(
                    brands, str) else 'brand__brand_name__in'
                queryset = queryset.filter(
                    Q(**{lookup: brands})
                )

            qs_filters = []
            for key, value in filters.items():
                attr_name, attr_values = {}, {}
                attr_name['attribute__attribute_name'] = key
                attr_values['attribute__attribute_value' if isinstance(
                    value, str) else 'attribute__attribute_value__in'] = value
                qs_filters.append(Q(**attr_name, **attr_values))

            queryset = queryset.filter(*qs_filters)

        queryset = queryset.annotate(rating=Avg(
            'reviews__product_rating')).select_related('brand').prefetch_related('available_shipping_types').order_by(
            '-updated_at', '-created_at')

        queryset = queryset.prefetch_related(Prefetch(
            'discounts', queryset=ProductDiscount.objects.order_by('discount_unit')))

        return queryset


class Product(models.Model):
    product_name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(
        _('Description'), blank=True, null=True)
    category = models.ManyToManyField('Category')
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.PROTECT,
        related_name='product',
        null=True,
        blank=True
    )
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField('Features', blank=True)
    coupon = models.ManyToManyField('Coupon', blank=True)
    attribute = models.ManyToManyField('Attribute', blank=True)
    available_shipping_types = models.ManyToManyField(
        ShippingType, blank=True)
    sku = models.IntegerField(unique=True)
    slug = models.SlugField(blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def __str__(self) -> str:
        return f"{self.product_name}"


class Category(MPTTModel):
    category_name = models.CharField(
        _('Category Name'), max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='categories', max_length=255)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='children')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['category_name']

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return f"{self.category_name}"


class Brand(models.Model):
    brand_name = models.CharField(_("Brand Name"), max_length=255, unique=True)
    slug = models.SlugField(blank=True, max_length=255, unique=True)
    image = models.ImageField(upload_to='brands', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.brand_name}"


class Attribute(models.Model):
    attribute_name = models.CharField(_('Attribute Name'), max_length=255)
    attribute_value = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Attributes'

    def __str__(self) -> str:
        return f"{self.attribute_name}: {self.attribute_value}"


class Features(models.Model):
    feature_description = models.TextField(_('Feature Description'))

    class Meta:
        verbose_name_plural = 'Features'

    def __str__(self) -> str:
        return f"{self.feature_description}"


class Coupon(models.Model):
    code = models.CharField(_('Coupon Code'), max_length=255)
    coupon_description = models.TextField(
        _('Coupon Description'), blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(_('Discount Type'), max_length=50)
    max_usage = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    expire_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.coupon_description}"


class ProductDiscount(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='discounts')
    discount_description = models.TextField(_('Discount Description'))
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_unit = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    expire_date = models.DateTimeField(blank=True, null=True)
    manimum_order_value = models.IntegerField(
        validators=[MinValueValidator(1)])
    maximum_order_value = models.IntegerField()

    def __str__(self) -> str:
        return f"Discount for: {self.product.product_name}"


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    url = models.ImageField(upload_to='products')
    alternative_text = models.CharField(
        max_length=50, blank=True, null=True)
    is_default = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Images'

    def __str__(self) -> str:
        return f"Image for {self.product}"
