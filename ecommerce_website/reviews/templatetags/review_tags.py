from django import template
from reviews.models import Review, ReviewRating

register = template.Library()


@register.simple_tag
def is_liked(user, review, is_like):
    return ReviewRating.objects.filter(
        user=user,
        review__id=review,
        is_like=is_like
    ).exists()
