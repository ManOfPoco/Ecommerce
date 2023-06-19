from typing import Any
from django.shortcuts import render

from products.models import Product, Category
from cart.models import CartItem

from cart.mixins import CartItemsCountMixin

from django.views.generic import TemplateView


def home(request):
    products = Product.objects.get_popular_products()
    categories = Category.objects.filter(mptt_level=0, is_active=True)

    context = {
        'products': products,
        'categories': categories,
        'cart_items_count': CartItem.objects.get_cart_items_count(request)
    }

    return render(request, 'home.html', context)


class DealsListView(CartItemsCountMixin, TemplateView):
    template_name = 'deals.html'


def my_custom_page_not_found_view(request, exception):
    products = Product.objects.get_popular_products()
    context = {
        'products': products,
        'cart_items_count': CartItem.objects.get_cart_items_count(request)
    }
    return render(request, '404.html', status=404, context=context)
