from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView
from django.views import View

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .models import Cart, CartItem, SaveForLater
from django.db.models.functions import Coalesce
from products.models import Product, ProductDiscount
from ecommerce.models import Shop

from ecommerce_website.decorators import is_ajax
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

from decimal import Decimal, InvalidOperation


class CartListView(ListView):
    model = CartItem
    context_object_name = 'cart_items'
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart.objects.get(user=self.request.user)
        save_for_later = SaveForLater.objects.get_cart_products(cart)
        bill = CartItem.objects.calculate_bill(self.get_queryset())
        pickup_shops = Shop.objects.all()

        context['not_available_products'] = getattr(
            self, 'not_available_products')
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


class CartItemsFormView(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):

        if 'new_quantity' in request.POST:
            cart = get_object_or_404(Cart, user=request.user)
            product = get_object_or_404(
                Product, slug=request.POST.get('product_slug'))
            item = get_object_or_404(CartItem, cart=cart, product=product)

            try:
                new_quantity = int(request.POST.get('new_quantity'))
            except ValueError:
                return HttpResponseBadRequest('Invalid quantity')

            if new_quantity > product.quantity:
                return JsonResponse({'success': False, 'status': 'Not enough products'})

            item.quantity = new_quantity
            item.save()

            base_product_price = item.product.regular_price * new_quantity
            current_price = ProductDiscount.objects.get_best_discount_price(item=item)[
                0]['discount_price'] * new_quantity if ProductDiscount.objects.get_best_discount_price(item=item) else base_product_price

            try:
                discount_amount = Decimal(request.POST.get('discount_amount'))
            except InvalidOperation:
                discount_amount = Decimal(0)

            base_bill_price = Decimal(request.POST.get('total_price'))
            product_old_price = Decimal(request.POST.get('old_price'))

            bill = {}
            bill['current_price'] = current_price
            bill['base_product_price'] = base_product_price
            bill['discount_amount'] = discount_amount if base_product_price == current_price else base_product_price - current_price

            if base_product_price == current_price:
                bill['bill_base_price'] = base_bill_price - \
                    product_old_price + base_product_price
                bill['bill_discount_price'] = base_bill_price - \
                    product_old_price + current_price - discount_amount
            else:
                bill['bill_discount_price'] = base_bill_price - \
                    (product_old_price + discount_amount) + current_price
                bill['bill_base_price'] = base_bill_price - \
                    (product_old_price + discount_amount) + base_product_price

            # add order price later
            bill['total_price'] = bill['bill_discount_price']

            return JsonResponse({
                'success': True,
                'status': 'Quantity changed',
                'bill': bill
            })


class CartItemRemove(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        get_object_or_404(CartItem,
                          cart__user=request.user,
                          product__slug=request.POST.get('product_slug')).delete()
        return JsonResponse({'success': True})


class SaveForLaterRemove(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        get_object_or_404(SaveForLater,
                          cart__user=request.user,
                          product__slug=request.POST.get('product_slug')).delete()
        return JsonResponse({'success': True})


class SaveForLaterCreate(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        product_slug = request.POST.get('product_slug')

        get_object_or_404(CartItem,
                          cart=cart,
                          product__slug=request.POST.get('product_slug')).delete()
        try:
            SaveForLater.objects.create(
                cart=cart,
                product=get_object_or_404(Product, slug=product_slug)
            )
        except IntegrityError:
            return JsonResponse({'success': False, 'status': 'Objects already exists'})
        return JsonResponse({'success': True, 'status': 'Moved successfully'})


class MoveToCart(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        product_slug = request.POST.get('product_slug')

        try:
            SaveForLater.objects.get(cart=cart,
                                     product__slug=request.POST.get('product_slug')).delete()
        except ObjectDoesNotExist:
            pass

        try:
            CartItem.objects.create(
                cart=cart,
                product=get_object_or_404(Product, slug=product_slug),
                quantity=1,
                pickup_shop=Shop.objects.get(id=1)
            )
        except IntegrityError:
            return JsonResponse({'success': False, 'status': 'Object already exists'})
        return JsonResponse({'success': True, 'status': 'Moved successfully'})


class CartView(View):

    def get(self, request, *args, **kwargs):
        view = CartListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CartItemsFormView.as_view()
        return view(request, *args, **kwargs)
