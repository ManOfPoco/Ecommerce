from django.shortcuts import render

from django.views.generic import ListView

from .models import Cart, CartItem, SaveForLater
from products.models import Product
from ecommerce.models import Shop


class CartView(ListView):
    model = CartItem
    context_object_name = 'cart_items'
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart.objects.get(user=self.request.user)
        save_for_later = SaveForLater.objects.get_cart_products(cart)
        bill = CartItem.objects.calculate_bill(self.get_queryset())
        pickup_shops = Shop.objects.all()

        context['not_available_products'] = getattr(self, 'not_available_products')
        context['pickup_shops'] = pickup_shops
        context['save_for_later_items'] = save_for_later
        context['bill'] = bill
        context['popular_products'] = Product.objects.get_popular_products()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        cart = Cart.objects.get(user=self.request.user)

        queryset = self.model.objects.get_cart_products(cart)
        queryset = self.model.objects.check_availability(queryset, self)

        return queryset
