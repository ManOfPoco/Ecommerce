from django.shortcuts import render, get_object_or_404

from payment_paypal.payment import create_payment_form

from django.views.generic import ListView
from django.views import View

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .models import Cart, CartItem, SaveForLater
from products.models import Product
from ecommerce.models import Shop

from ecommerce_website.decorators import is_ajax
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseBadRequest


class CartListView(ListView):
    model = CartItem
    context_object_name = 'cart_items'
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart.objects.get_or_create_cart(self.request)
        save_for_later = SaveForLater.objects.get_cart_products(cart)
        bill = CartItem.objects.calculate_bill(self.get_queryset())
        pickup_shops = Shop.objects.all()
        payment_form = create_payment_form(self.request, self.get_queryset().count(), total_price=bill['total_price'])

        context['not_available_products'] = getattr(
            self, 'not_available_products')
        context['pickup_shops'] = pickup_shops
        context['save_for_later_items'] = save_for_later
        context['bill'] = bill
        context['popular_products'] = Product.objects.get_popular_products()
        context['cart_items_count'] = CartItem.objects.get_cart_items_count(
            self.request)
        context['payment_form'] = payment_form

        return context

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):

        cart = Cart.objects.get_or_create_cart(request)
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

        queryset = self.get_queryset()
        bill = self.model.objects.calculate_bill(queryset)
        product = queryset.get(product=product)

        return JsonResponse({
            'success': True,
            'status': 'Quantity changed',
            'product': {
                'base_price': round(product.base_price, 2),
                'discount_price': round(product.current_price, 2)
            },
            'bill': bill
        })

    def get_queryset(self):
        queryset = super().get_queryset()
        cart = Cart.objects.get_or_create_cart(self.request)

        queryset = self.model.objects.get_cart_products(cart)
        queryset = self.model.objects.check_availability(queryset, self)

        return queryset


class CartItemRemove(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get_or_create_cart(request)
        get_object_or_404(CartItem,
                          cart=cart,
                          product__slug=request.POST.get('product_slug')).delete()
        return JsonResponse({'success': True})


class SaveForLaterRemove(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get_or_create_cart(request)
        get_object_or_404(SaveForLater,
                          cart=cart,
                          product__slug=request.POST.get('product_slug')).delete()
        return JsonResponse({'success': True})


class SaveForLaterCreate(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        cart = Cart.objects.get_or_create_cart(request)

        try:
            CartItem.objects.get(
                cart=cart,
                product__id=product_id).delete()
        except CartItem.DoesNotExist:
            pass

        try:
            SaveForLater.objects.create(
                cart=cart,
                product=get_object_or_404(Product, id=product_id)
            )
        except IntegrityError:
            return JsonResponse({'success': False, 'status': 'Object already exists in your Save For Later cart section'})
        return JsonResponse({'success': True, 'status': 'Added successfully'})


class MoveToCart(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        cart = Cart.objects.get_or_create_cart(request)
        try:
            SaveForLater.objects.get(
                cart=cart, product__id=request.POST.get('product_id')).delete()
        except ObjectDoesNotExist:
            pass

        try:
            CartItem.objects.create(
                cart=cart,
                product=get_object_or_404(Product, id=product_id),
                quantity=quantity or 1,
                pickup_shop=Shop.objects.get(id=1)
            )
        except IntegrityError:
            return JsonResponse({'success': False, 'status': 'Object already exists in your cart'})

        return JsonResponse({'success': True, 'status': 'Added successfully'})
