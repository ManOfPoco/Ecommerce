from django.shortcuts import render
from django.db.models import Q, Avg, Count, Prefetch

from products.filters import get_default_filters
from products.models import Product, ProductImages, ProductDiscount

from cart.mixins import CartItemsCountMixin

from django.views.generic import ListView

from wishlist.forms import WishListItemAddForm


class SearchView(CartItemsCountMixin, ListView):
    template_name = 'search/search.html'
    context_object_name = 'product_page'
    model = Product
    paginate_by = 24

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        default_filters = get_default_filters(self.get_queryset())

        context['default_filters'] = default_filters

        if self.request.user.is_authenticated:
            context['wishlist_item_add_form'] = WishListItemAddForm(
                self.request.user)

        return context

    def get_queryset(self):

        queryset = super().get_queryset()

        query_dict = self.request.GET

        query = query_dict.get('q', None)
        queryset = Product.objects.filter(
            Q(is_active=True) &
            Q(product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__brand_name__icontains=query) |
            Q(features__feature_description__icontains=query) |
            Q(attribute__attribute_name__icontains=query)
        )
        queryset = queryset.annotate(rating=Avg(
            'reviews__product_rating'), reviews_count=Count('reviews__product_rating')
        ).distinct()

        selected_filters = {
            key: query_dict.getlist(key)[0]
            if len(query_dict.getlist(key)) == 1 else query_dict.getlist(key)
            for key in query_dict
            if key != 'q' and key != 'ordering' and key != 'page'
        }

        queryset = Product.objects.filter_products_by(
            queryset, selected_filters)

        queryset = queryset.select_related('brand').prefetch_related(
            'available_shipping_types',
            Prefetch(
                'images', queryset=ProductImages.objects.filter(is_default=True)),
            Prefetch(
                'discounts', queryset=ProductDiscount.objects.get_discounts(), to_attr='product_discounts')
        )
        ordering = self.request.GET.get('ordering', 'features')
        queryset = Product.objects.order_product_by(queryset, ordering)

        return queryset
