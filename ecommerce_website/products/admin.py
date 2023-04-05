from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import (
    Product,
    Brand,
    Category,
    Features,
    Coupon,

    Attribute,
    AttributeValue,
    ProductImages,
    ProductDiscount,
    ShippingType,
)


class ImagesInline(admin.StackedInline):
    model = ProductImages
    extra = 3

    prepopulated_fields = {'alternative_text': ('url',)}


class ProductDiscountInline(admin.StackedInline):
    model = ProductDiscount
    extra = 2


class ProductAttributeInline(admin.StackedInline):
    model = Product.attribute.through
    fields = ('attribute', )
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        ('product_name', 'slug'),
        'description',
        'category',
        'brand',
        'regular_price',
        'coupon',
        'available_shipping_types',
        'sku',
        'is_active',
        'quantity',
    ]

    prepopulated_fields = {
        'slug': ('product_name',)}
    filter_horizontal = ['category', 'features',
                         'coupon', 'available_shipping_types']

    inlines = [
        ProductAttributeInline,
        ImagesInline,
        ProductDiscountInline,
    ]


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    extra = 2


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline, ]


class CategoryInline(admin.StackedInline):
    model = Category
    extra = 2

    fields = [('category_name', 'slug'), 'image', 'is_active']
    prepopulated_fields = {'slug': ('category_name',)}

    verbose_name = 'Child Category'
    verbose_name_plural = 'Child Categories'


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    fields = [('category_name', 'slug'), 'image', 'is_active']

    list_display = [
        'category_name',
        'created_at',
        'updated_at'
    ]

    mptt_level_indent = 20

    inlines = [CategoryInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fields = [('brand_name', 'slug'), 'image']

    prepopulated_fields = {'slug': ('brand_name',)}


admin.site.register(Features)
admin.site.register(Coupon)
admin.site.register(ProductDiscount)
admin.site.register(ProductImages)
