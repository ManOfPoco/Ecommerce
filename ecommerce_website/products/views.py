from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.core.paginator import Paginator

from django.db.models import Prefetch, Avg, Count

from . import services
from . import filters

from .models import Category, Product, ProductDiscount
from reviews.models import Review


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
                        categories=category.get_descendants())
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


class ProductView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_overview.html'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        category = product.category.first()
        category_ancestors = category.get_ancestors(include_self=True)

        product_reviews_rating = Review.objects.aggregate_product_reviews(
            product)
        reviews = Review.objects.prefetch_review_ratings(product)

        most_liked_positive_review = Review.objects.get_most_liked_positive_product_review(
            product)
        most_liked_negative_review = Review.objects.get_most_liked_negative_product_review(
            product)

        context['ancestors'] = category_ancestors
        context['product_reviews_rating'] = product_reviews_rating
        context['reviews'] = reviews
        if most_liked_positive_review and most_liked_negative_review:
            context['most_liked_positive_review'] = most_liked_positive_review
            context['most_liked_negative_review'] = most_liked_negative_review

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('brand').prefetch_related(
            'images',
            'attribute',
            'features',
            'coupon',
            'available_shipping_types',
            Prefetch(
                'discounts', queryset=ProductDiscount.objects.order_by('discount_unit'))
        ).annotate(
            rating=Avg('reviews__product_rating'),
            reviews_count=Count('reviews__product_rating')
        )
        return queryset.filter(slug=self.kwargs.get('product_slug'))
