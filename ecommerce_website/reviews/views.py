from django.shortcuts import render, get_object_or_404

from django.views import View

from products.models import Product
from django.db.utils import IntegrityError

from .forms import ReviewForm

from django.http import JsonResponse

from ecommerce_website.decorators import is_ajax
from django.utils.decorators import method_decorator


class CreateReviewForm(View):

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST or None)
        try:
            if form.is_valid():
                form.instance.product = get_object_or_404(
                    Product, slug=request.POST.get('product'))
                form.instance.user = request.user
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False})
        except IntegrityError:
            return JsonResponse({'success': False})
