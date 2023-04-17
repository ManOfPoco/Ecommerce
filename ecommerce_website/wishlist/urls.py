from django.urls import path

from .views import WishListView, WishListDeleteView

app_name = 'wishlist'


urlpatterns = [
    path('', WishListView.as_view(), name='wishlist'),
    path('<slug:wishlist_slug>', WishListView.as_view(), name='wishlist-items'),
    path('delete/<slug:wishlist_slug>',
         WishListDeleteView.as_view(), name='delete-wishlist'),
]
