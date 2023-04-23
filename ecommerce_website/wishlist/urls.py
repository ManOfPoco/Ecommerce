from django.urls import path

from .views import (
    WishListView,
    WishListDeleteView,
    WishListItemDeleteView,
    WishLishAddView
)

app_name = 'wishlist'


urlpatterns = [
    path('wishlist-delete/', WishListDeleteView.as_view(), name='wishlist-delete'),
    path('wishlist-item-delete/', WishListItemDeleteView.as_view(),
         name='wishlist-item-delete'),
    path('wishlist-add/', WishLishAddView.as_view(), name='wishlist-add'),
    path('', WishListView.as_view(), name='wishlist'),
    path('<slug:wishlist_slug>/', WishListView.as_view(), name='wishlist-items'),
]
