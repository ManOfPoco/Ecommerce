from django.db import models
from django.db.models import Count, Q

from django.contrib.auth.models import User
from products.models import Product

from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.translation import gettext_lazy as _


class ReviewManager(models.Manager):

    def aggregate_product_reviews(self, product):
        queryset = product.reviews.aggregate(
            five_stars=Count('product_rating', filter=Q(product_rating=5)),
            four_stars=Count('product_rating', filter=Q(product_rating=4)),
            three_stars=Count('product_rating', filter=Q(product_rating=3)),
            two_stars=Count('product_rating', filter=Q(product_rating=2)),
            one_star=Count('product_rating', filter=Q(product_rating=1)),
        )

        return queryset

    def prefetch_review_ratings(self, product, ordering='recent'):

        queryset = product.reviews.prefetch_related(
            'rating').annotate(likes=Count('rating', filter=Q(rating__is_like=True)),
                               dislikes=Count('rating', filter=Q(rating__is_like=False)))

        review_ordering_types = {
            'recent': queryset.order_by('-created_at', '-updated_at'),
            'helpful': queryset.order_by('-product_rating', '-likes'),
            'lowest': queryset.order_by('product_rating', '-dislikes'),
            'highest': queryset.order_by('-product_rating', '-likes'),
            'oldest': queryset.order_by('created_at')
        }

        queryset = review_ordering_types.get(
            ordering, queryset.order_by('-created_at'))

        return queryset

    def get_most_liked_positive_product_review(self, product):
        queryset = product.reviews.filter(
            rating__is_like=True, product_rating__gte=3).order_by('-rating__is_like').first()

        return queryset

    def get_most_liked_negative_product_review(self, product):
        queryset = product.reviews.filter(
            rating__is_like=True, product_rating__lt=3).order_by('-rating__is_like').first()

        return queryset


class Review(models.Model):
    BOTTOM_LINE_CHOICES = [
        ('yes', 'Yes, I would recommend this to a friend'),
        ('no', 'No, I would not recommend this to a friend')
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reveiws')
    headline = models.CharField(_('Headline'), max_length=100)
    body = models.TextField(_('Body'))
    bottom_line = models.CharField(
        _('Bottom Line'), max_length=3, choices=BOTTOM_LINE_CHOICES)
    product_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['product', 'user'],
            name='unique_user_review',
            violation_error_message=f"Each user can review"
            f"each product only once"
        )]

    def __str__(self) -> str:
        return f"{self.headline}"


class ReviewRating(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rating')
    is_like = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['review', 'user'],
            name='unique_user_review_rating',
            violation_error_message=f"Each user can rate review only once"
        )]

    def __str__(self) -> str:
        return f"{self.is_like}"
