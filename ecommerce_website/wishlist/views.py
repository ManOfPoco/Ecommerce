from django.shortcuts import render

from django.views.generic import ListView, DeleteView, FormView
from django.views import View

from .models import WishList, WishListItem
from products.models import Product

from .forms import WishlistForm

from ecommerce_website.decorators import is_ajax
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from django.core.exceptions import ObjectDoesNotExist

from django.template.defaultfilters import slugify


class WishListListView(ListView):
    model = WishList
    template_name = 'wishlist/wishlist.html'
    context_object_name = 'wishlists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if slug := self.kwargs.get('wishlist_slug'):
            wishlist = WishList.objects.get(slug=slug)
            context['wishlist_update_form'] = WishlistForm(instance=wishlist)
        else:
            wishlist = WishList.objects.get(is_default=True)

        ordering = self.request.GET.get('ordering', 'date-added')
        wishlist_items = WishListItem.objects.get_wishlist_products(
            wishlist, ordering)

        context['wishlist'] = wishlist
        context['wishlist_form'] = WishlistForm()
        context['wishlist_items'] = wishlist_items
        context['popular_products'] = Product.objects.get_popular_products()
        return context


class WishlistChangeView(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        form = WishlistForm(request.POST or None)
        try:
            wishlist = WishList.objects.get(
                slug=request.POST.get('wishlist_slug'))

            wishlist.list_name = request.POST.get('list_name')
            wishlist.slug = slugify(request.POST.get('list_name'))

            if request.POST.get('is_default'):
                default_wishlist = WishList.objects.filter(
                    is_default=True).first()
                default_wishlist.is_default = False
                default_wishlist.save()

                wishlist.is_default = True

            wishlist.save()
            return JsonResponse({'success': True, 'slug': wishlist.slug})

        except ObjectDoesNotExist:
            if form.is_valid():
                form.instance.user = request.user

                if request.POST.get('is_default', False):
                    default_wishlist = WishList.objects.filter(
                        is_default=True).first()
                    if default_wishlist:
                        default_wishlist.is_default = False
                        default_wishlist.save()

                form.save()
                return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class WishListView(View):
    def get(self, request, *args, **kwargs):
        view = WishListListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'item_deletion' in request.POST:
            view = WishListItemDeleteView.as_view()
        elif 'wishlist_deletion' in request.POST:
            view = WishListDeleteView.as_view()
        else:
            view = WishlistChangeView.as_view()
        return view(request, *args, **kwargs)


class WishListDeleteView(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):

        user = request.user
        slug = request.POST.get('wishlist_slug')

        WishList.objects.get(
            user=user, slug=slug).delete()

        default_slug = WishList.objects.get(is_default=True).slug
        return JsonResponse({'success': True, 'slug': default_slug})


class WishListItemDeleteView(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        wishlist = WishList.objects.get(id=request.POST.get('wishlist'))
        product = Product.objects.get(slug=request.POST.get('product'))

        WishListItem.objects.get(
            product=product, wishlist=wishlist).delete()

        return JsonResponse({'success': True})
