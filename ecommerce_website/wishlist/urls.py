from django.urls import path

from .views import WishListView, WishListDeleteView, WishListItemDeleteView

app_name = 'wishlist'


urlpatterns = [
    path('', WishListView.as_view(), name='wishlist'),
    path('my-wishlist/<slug:wishlist_slug>', WishListView.as_view(), name='wishlist-items'),
    path('wishlist-delete/', WishListDeleteView.as_view(), name='wishlist-delete'),
    path('wishlist-item-delete/', WishListItemDeleteView.as_view(), name='wishlist-item-delete'),
]
