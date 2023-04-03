from django.shortcuts import render

from django.db.models import OuterRef, Subquery, Prefetch, Q, DecimalField
from products.models import (
    Product,
    ProductDiscount,
    ProductImages,
    Category
)

from decimal import Decimal


def home(request):

    discount_price_subquery = ProductDiscount.objects.filter(
        product=OuterRef('pk'), discount_unit=1
    ).order_by('discount_price').values('discount_price')[:1]

    default_image_subquery = ProductImages.objects.filter(
        product=OuterRef('pk'), is_default=True
    ).values('id')[:1]

    products = Product.objects.annotate(
        discount=Subquery(discount_price_subquery)
    ).filter(is_active=True).prefetch_related(
        Prefetch('images',
                 queryset=ProductImages.objects.filter(
                     Q(pk__in=Subquery(default_image_subquery)))))[:10]

    categories = Category.objects.all()

    categories = context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'home.html', context)
