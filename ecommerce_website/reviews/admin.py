from django.contrib import admin
from .models import Review, ReviewRating

admin.site.register(Review)
admin.site.register(ReviewRating)