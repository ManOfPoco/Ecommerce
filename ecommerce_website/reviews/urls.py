from django.urls import path

from .views import CreateReviewForm, ReviewRatingView

app_name = 'reviews'


urlpatterns = [
    path('write-review/', CreateReviewForm.as_view(), name='create-review'),
    path('rate-review/', ReviewRatingView.as_view(), name='rate-review'),
]
