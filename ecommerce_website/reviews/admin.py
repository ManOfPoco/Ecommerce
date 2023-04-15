from django.contrib import admin
from .models import Review, ReviewRating


admin.site.register(ReviewRating)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['headline', 'created_at']
