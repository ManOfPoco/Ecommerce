from django.shortcuts import render

from products.models import (
    Product,
    Category
)


def home(request):
    products = Product.objects.get_popular_products()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'home.html', context)


def my_custom_page_not_found_view(request, exception):
    products = Product.objects.get_popular_products()
    context = {
        'products': products
    }
    return render(request, '404.html', status=404, context=context)
