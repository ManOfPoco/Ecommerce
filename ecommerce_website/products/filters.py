from django.db.models import Count, Q, Max, Avg
from .models import Product, Brand

from django.core.cache import cache

from django.template.defaultfilters import slugify

from collections import defaultdict


def get_default_filters(categories, products):
    default_filters = defaultdict(list)

    brands = Product.objects.get_unique_product_brands(
        categories, include_count=True)
    default_filters['Brand'].extend([brand for brand in brands])

    default_filters['Price'] = products.aggregate(
        max_price=Max('regular_price'))['max_price']

    products = products.annotate(
        rating=Avg('reviews__product_rating'))
    default_filters['Customer Reviews'] = products.aggregate(
        five_stars=Count('rating',
                         filter=Q(rating__gt=5)),
        four_stars=Count('rating',
                         filter=Q(rating__gt=4)),
        three_stars=Count('rating',
                          filter=Q(rating__gt=3)),
        two_stars=Count('rating',
                        filter=Q(rating__gt=2)),
        one_star=Count('rating',
                       filter=Q(rating__gt=1)),
    )

    default_filters.default_factory = None
    return default_filters


def get_specific_filters(products):
    specific_filters = defaultdict(list)

    for product in products:
        for product_filter in product.attribute.all():
            filter_name = product_filter.attribute_name
            if product_filter.attribute_value not in specific_filters[filter_name]:
                specific_filters[filter_name].append(
                    product_filter.attribute_value)

    specific_filters.default_factory = None
    return specific_filters


def get_filters(categories):
    filters = cache.get(
        f'CACHED_FILTERS_FOR_{slugify(categories.first().category_name)}'
    )
    if filters is None:
        filters = defaultdict(dict)
        products = Product.objects.filter(category__in=categories
                                          ).prefetch_related('attribute')
        default_filters, specific_filters = get_default_filters(
            categories, products), get_specific_filters(products)

        filters['default_filters'], filters['specific_filters'] = default_filters, specific_filters
        cache.set(
            f'CACHED_FILTERS_FOR_{slugify(categories.first().category_name)}', filters, 60*60
        )
    return filters
