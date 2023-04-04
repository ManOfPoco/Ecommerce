from django.shortcuts import render
from django.views.generic import TemplateView
from . import services

from .models import Category, Product


class CategoryView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = kwargs.get('slug')
        category = Category.objects.get(slug=slug)

        children = category.get_children(
        ).prefetch_related('children__children')
        for child in children:
            key = child.slug.replace('-', '_')
            context[key] = child.children.all()

        category_params = services.CATEGORY_PARAMS.get(slug, {})
        for key, value in category_params.items():
            if value:
                if key == 'brands':
                    context[key] = Product.objects.unique_brands_in_category(
                        category)
                elif key == 'products':
                    context[key] = Product.objects.get_popular_products()
                elif key == 'size':
                    context[key] = value

        return context

    def get_template_names(self):
        return [f"products/{self.kwargs.get('slug')}.html"]
