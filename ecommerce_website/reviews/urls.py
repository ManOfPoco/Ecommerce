from django.urls import path

from .views import CreateReviewForm

app_name = 'reviews'


urlpatterns = [
    path('write-review/', CreateReviewForm.as_view(), name='create-review')
]
