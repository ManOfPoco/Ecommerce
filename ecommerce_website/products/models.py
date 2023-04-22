from django.db import models
from django.db.models import Prefetch, Avg, Count, Q, OuterRef

from mptt.models import MPTTModel, TreeForeignKey
from shippings.models import ShippingType

from django.core.validators import MinValueValidator

from django.utils.translation import gettext_lazy as _

from django.core.cache import cache
from django.http import Http404

from django.template.defaultfilters import slugify

from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.utils.timezone import make_aware


class ProductManager(models.Manager):

    def get_popular_products(self, category=None):
        queryset = self.filter(is_active=True).select_related('brand').prefetch_related(
            Prefetch('images', queryset=ProductImages.objects.filter(is_default=True)))

        queryset = queryset.prefetch_related(Prefetch(
            'discounts', queryset=ProductDiscount.objects.order_by("-discount_unit")))

        if category:
            categories = category.get_descendants(include_self=True)
            queryset = queryset.filter(category__in=categories)

        return queryset[:10]

    def get_unique_product_brands(self, categories, include_count=False):
        brands = cache.get(
            f'CACHED_BRANDS_FOR_{slugify(categories.first().category_name)}'
        )

        if brands is None:
            brands = Brand.objects.filter(
                product__category__in=categories).distinct()

            if include_count:
                brands = brands.annotate(count=Count(
                    'product', filter=Q(product__category__in=categories)))

            cache.set(
                f'CACHED_BRANDS_FOR_{slugify(categories.first().category_name)}', brands, 60*60)

        return brands

    def get_products(self, categories, filter_params=None, ordering='features'):
        queryset = self.filter(
            category__in=categories, is_active=True)

        if filter_params:
            min_price, max_price = filter_params.pop(
                'min_price', None), filter_params.pop('max_price', None)
            if min_price and max_price:
                try:
                    min_price, max_price = Decimal(
                        min_price), Decimal(max_price)
                except InvalidOperation:
                    raise Http404

                queryset = queryset.filter(
                    regular_price__range=(min_price, max_price))

            reviews = filter_params.pop('reviews', None)
            if reviews and isinstance(reviews, (list, str)):
                try:
                    rating = min(reviews) if isinstance(
                        reviews, list) else int(reviews)
                except ValueError:
                    raise Http404

                queryset = queryset.filter(
                    reviews__product_rating__gte=rating)

            brand = filter_params.pop('Brand', None)
            if brand:
                lookup = 'brand__brand_name' if isinstance(
                    brand, str) else 'brand__brand_name__in'
                queryset = queryset.filter(
                    Q(**{lookup: brand})
                )

            attribute_filters = []
            for key, value in filter_params.items():
                if isinstance(value, str):
                    attr_filter = Q(attribute__attribute_name=key,
                                    attribute__attribute_value=value)
                elif isinstance(value, list):
                    attr_filter = Q(attribute__attribute_name=key,
                                    attribute__attribute_value__in=value)
                else:
                    raise Http404
                attribute_filters.append(attr_filter)

            queryset = queryset.filter(*attribute_filters)

        queryset = queryset.annotate(rating=Avg(
            'reviews__product_rating'), reviews_count=Count('reviews__product_rating')
        ).select_related('brand').prefetch_related(
            'available_shipping_types',
            Prefetch(
                'images', queryset=ProductImages.objects.filter(is_default=True)),
            Prefetch(
                'discounts', queryset=ProductDiscount.objects.get_discounts(), to_attr='product_discounts')
        )
        product_ordering_types = {
            'features': queryset.order_by('quantity'),  # temporarily
            'price_up': queryset.order_by('regular_price'),
            'price_down': queryset.order_by('-regular_price'),
            'newest': queryset.order_by('-created_at', '-updated_at'),
            'name_ascending': queryset.order_by('product_name'),
            'name_descending': queryset.order_by('-product_name'),
        }
        queryset = product_ordering_types.get(ordering)

        return queryset


class ProductDiscountManager(models.Manager):

    def get_discounts(self, product_slug=None):
        today = make_aware(datetime.now())
        discounts = ProductDiscount.objects.filter(
            Q(start_date__lte=today) &
            Q(expire_date__gte=today))

        if product_slug:
            discounts = discounts.filter(
                Q(product__slug=product_slug))

        return discounts.order_by("-discount_unit")

    def get_best_discount_price(self, item=None):
        today = make_aware(datetime.now())
        if not item:
            discount_price = ProductDiscount.objects.filter(
                Q(product=OuterRef('product')) &
                Q(start_date__lte=today) &
                Q(expire_date__gte=today) &
                Q(minimum_order_value__lte=OuterRef('quantity')) &
                Q(maximum_order_value__gte=OuterRef('quantity'))
            ).order_by("-discount_unit").values('discount_price')

        else:
            discount_price = ProductDiscount.objects.filter(
                Q(product=item.product) &
                Q(start_date__lte=today) &
                Q(expire_date__gte=today) &
                Q(minimum_order_value__lte=item.quantity) &
                Q(maximum_order_value__gte=item.quantity)
            ).order_by("-discount_unit").values('discount_price')

        return discount_price[:1]


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
    minimum_order_value = models.IntegerField(
        validators=[MinValueValidator(1)])
    maximum_order_value = models.IntegerField()

    objects = ProductDiscountManager()

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
