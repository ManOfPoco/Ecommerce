from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.core.paginator import Paginator

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
    category_descendants = category.get_descendants(
        include_self=True)

    if request.method == 'GET':
        query_dict = request.GET
        query_dict._mutable = True
        page_number = query_dict.pop('page', 1)
        ordering = query_dict.pop('ordering', None)

        selected_filters = {key: query_dict.getlist(key)[0] if len(query_dict.getlist(
            key)) == 1 else query_dict.getlist(key) for key in query_dict}

        if ordering:
            products = Product.objects.get_products(
                category_descendants,
                filter_params=selected_filters,
                ordering=ordering[0]
            )
        else:
            products = Product.objects.get_products(
                category_descendants,
                filter_params=selected_filters
            )

        product_filters = filters.get_filters(category_descendants)
        paginator = Paginator(products, 24)

        try:
            page_number = int(page_number[0])
        except TypeError:
            page_number = 1
        page = paginator.get_page(page_number)

        popular_products = Product.objects.get_popular_products()

        context = {
            'category': category,
            'ancestors': category_ancestors,
            'subcategories': category_children,
            'popular_products': popular_products,
            'page': page,
            'default_filters': product_filters['default_filters'],
            'specific_filters': product_filters['specific_filters'],
        }

        return render(request, 'products/products.html', context)
