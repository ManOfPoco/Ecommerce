from django.db.models import Count, Q, Max
from .models import Product, Brand

from django.core.cache import cache

from django.template.defaultfilters import slugify

from collections import defaultdict


def get_default_filters(category, products):
    default_filters = defaultdict(list)

    brands = Product.objects.get_unique_product_brands(
        category, include_count=True)

    default_filters['Brand'].extend([brand for brand in brands])
    default_filters['Price'] = products.aggregate(
        max_price=Max('regular_price'))['max_price']
    default_filters['Customer Reviews'] = products.aggregate(
        one_star=Count('reviews__product_rating',
                       filter=Q(reviews__product_rating=1)),
        two_stars=Count('reviews__product_rating',
                        filter=Q(reviews__product_rating=2)),
        three_stars=Count('reviews__product_rating',
                          filter=Q(reviews__product_rating=3)),
        four_stars=Count('reviews__product_rating',
                         filter=Q(reviews__product_rating=4)),
        five_stars=Count('reviews__product_rating',
                         filter=Q(reviews__product_rating=5)),
    )

    default_filters.default_factory = None
    return default_filters


def get_specific_filters(products):
    specific_filters = defaultdict(list)

    for product in products:
        for product_filter in product.attribute.all():
            filter_name = product_filter.attribute_name.title()
            if product_filter.attribute_value and \
                    product_filter.attribute_value not in specific_filters[filter_name]:
                specific_filters[filter_name].append(
                    product_filter.attribute_value)

    specific_filters.default_factory = None
    return specific_filters


def get_filters(category):
    filters = cache.get(
        f'CACHED_FILTERS_FOR_{slugify(category.category_name)}'
    )
    if filters is None:
        filters = defaultdict(dict)
        products = Product.objects.filter(category=category
                                          ).prefetch_related('attribute')

        default_filters, specific_filters = get_default_filters(
            category, products), get_specific_filters(products)

        filters['default_filters'], filters['specific_filters'] = default_filters, specific_filters
        cache.set(
            f'CACHED_FILTERS_FOR_{slugify(category.category_name)}', filters, 60*60
        )
    return filters
