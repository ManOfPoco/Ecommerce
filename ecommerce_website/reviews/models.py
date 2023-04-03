from django.db import models

from django.contrib.auth.models import User
from products.models import Product

from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.translation import gettext_lazy as _


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
