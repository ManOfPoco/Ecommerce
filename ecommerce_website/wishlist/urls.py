from django.urls import path

from .views import (
    WishListView,
    WishListDeleteView,
    WishListItemDeleteView,
    WishLishItemAddView
)

app_name = 'wishlist'


urlpatterns = [
    path('wishlist-delete/', WishListDeleteView.as_view(), name='wishlist-delete'),
    path('wishlist-item-delete/', WishListItemDeleteView.as_view(),
         name='wishlist-item-delete'),
    path('wishlist-item-add/', WishLishItemAddView.as_view(), name='wishlist-item-add'),
    path('', WishListView.as_view(), name='wishlist'),
    path('<int:id>/', WishListView.as_view(), name='wishlist-items'),
]
