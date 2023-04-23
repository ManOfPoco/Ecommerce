from django.shortcuts import render, get_object_or_404

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Review, ReviewRating
from products.models import Product
from django.db.utils import IntegrityError

from .forms import ReviewForm

from django.http import JsonResponse

from ecommerce_website.decorators import is_ajax
from django.utils.decorators import method_decorator


class ReviewRatingView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        return JsonResponse({}, status=302)

    @method_decorator(is_ajax)
    def post(self, request, *args, **kwargs):
        review = get_object_or_404(
            Review, id=request.POST.get('review_id'))
        is_like = request.POST.get('option') == 'like'

        try:
            instance = ReviewRating.objects.get(
                review=review, user=request.user)

            if instance.is_like and is_like or \
                    instance.is_like is False and is_like is False:
                instance.delete()
                status = 'Removed'

            elif instance.is_like and is_like is False or \
                    instance.is_like is False and is_like:
                instance.is_like = is_like
                instance.save()
                status = 'Changed'
            else:
                status = 'Error'

        except ReviewRating.DoesNotExist:
            ReviewRating.objects.create(
                review=review, user=request.user, is_like=is_like)
            status = 'Created'

        except IntegrityError:
            status = 'Something went wrong'

        return JsonResponse({'status': status})


class CreateReviewForm(LoginRequiredMixin, View):

    def handle_no_permission(self):
        return JsonResponse({}, status=302)

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
