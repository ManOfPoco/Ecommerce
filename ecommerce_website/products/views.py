from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from . import services
from . import filters

from .models import Category, Product


class CategoryView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=slug, mptt_level=0)

        category_params = services.CATEGORY_PARAMS.get(slug, {})
        category_children = category.get_children()

        if category_params['categories'] == 'subcategories':
            category_children = category_children.prefetch_related(
                'children__children')

            for child in category_children:
                key = child.slug.replace('-', '_')
                context[key] = child.children.all()
        else:
            context['categories'] = category_children

        for key, value in category_params.items():
            if value:
                if key == 'brands':
                    context[key] = Product.objects.get_unique_product_brands(
                        category)
                elif key == 'products':
                    context[key] = Product.objects.get_popular_products(
                        category=category)
                elif key == 'size':
                    context[key] = value

        return context

    def get_template_names(self):
        return [f"products/{self.kwargs.get('category_slug')}.html"]


def category_products(request, **kwargs):
    slug = kwargs.get('category_path').split('/')[-1]
    category = get_object_or_404(Category, slug=slug)
    category_children = category.get_children()
    category_ancestors = category.get_ancestors(include_self=True)

    if request.method == 'GET':
        selected_filters = {key: request.GET.getlist(key)[0] if len(request.GET.getlist(
            key)) == 1 else request.GET.getlist(key) for key in request.GET}

        products = Product.objects.get_products(
            category, filter_params=selected_filters)
        product_filters = filters.get_filters(category)
        popular_products = Product.objects.get_popular_products()

        context = {
            'category': category,
            'ancestors': category_ancestors,
            'subcategories': category_children,
            'popular_products': popular_products,
            'products': products,
            'default_filters': product_filters['default_filters'],
            'specific_filters': product_filters['specific_filters'],
        }

        return render(request, 'products/products.html', context)
