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
            wishlist.is_default = True if request.POST.get(
                'is_default') else wishlist.is_default

            wishlist.save()
            return JsonResponse({'success': True})

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
        if 'product' in request.POST and 'wishlist' in request.POST:
            view = WishListItemView.as_view()
        else:
            view = WishlistChangeView.as_view()
        return view(request, *args, **kwargs)


class WishListDeleteView(DeleteView):
    model = WishList
    success_url = "/wishlist/"
    slug_url_kwarg = 'wishlist_slug'


class WishListItemView(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        print(request.POST)

        wishlist = WishList.objects.get(slug=request.POST.get('wishlist'))
        product = Product.objects.get(slug=request.POST.get('product'))

        WishListItem.objects.get(
            product=product, wishlist=wishlist).delete()

        return JsonResponse({'success': True})
