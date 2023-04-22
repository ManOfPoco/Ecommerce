from django.shortcuts import render, get_object_or_404

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
        context['cart_items_count'] = CartItem.objects.count()

        return context

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):

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
        cart = Cart.objects.get(user=self.request.user)

        queryset = self.model.objects.get_cart_products(cart)
        queryset = self.model.objects.check_availability(queryset, self)

        return queryset


class CartItemsFormView(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):

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

        return JsonResponse({
            'success': True,
            'status': 'Quantity changed',
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
        return JsonResponse({'success': True, 'status': 'Added successfully'})
