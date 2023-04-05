from django.db import models
from django.db.models import Prefetch, Subquery, OuterRef

from mptt.models import MPTTModel, TreeForeignKey
from shippings.models import ShippingType

from django.core.validators import MinValueValidator

from django.utils.translation import gettext_lazy as _

from django.core.cache import cache


class ProductManager(models.Manager):
    def get_popular_products(self, category=None):
        discount_price_subquery = ProductDiscount.objects.filter(
            product=OuterRef('pk'), discount_unit=1
        ).order_by('discount_price').values('discount_price')[:1]

        queryset = self.annotate(
            discount=Subquery(discount_price_subquery)
        ).select_related('brand').filter(is_active=True).prefetch_related(
            Prefetch('images',
                     queryset=ProductImages.objects.filter(is_default=True)))

        if category:
            queryset = queryset.filter(category=category)

        return queryset[:10]

    def unique_brands_in_category(self, category):
        brands = cache.get(
            f'CACHED_BRANDS_FOR_{category.category_name.upper()}')
        if brands is None:
            brands = Product.objects.select_related('brand').filter(
                category=category).distinct()
            cache.set(
                f'CACHED_BRANDS_FOR_{category.category_name.upper()}', brands, 60*60)

        return brands


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
    category_name = models.CharField(_('Category Name'), max_length=255)
    slug = models.SlugField(max_length=255)
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
    brand_name = models.CharField(_("Brand Name"), max_length=255)
    slug = models.SlugField(blank=True, max_length=255)
    image = models.ImageField(upload_to='brands', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.brand_name}"


class Attribute(models.Model):
    attribute_name = models.CharField(_('Attribute Name'), max_length=255)

    class Meta:
        verbose_name_plural = 'Attributes'

    def __str__(self) -> str:
        return f"{self.attribute_name}"


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name='attribute_value')
    attribute_value = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Attribute Values'

    def __str__(self) -> str:
        return f"{self.attribute_value}"


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
