from .models import Cart, CartItem


class CartItemsCountMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items_count'] = CartItem.objects.get_cart_items_count(
            self.request)
        return context
