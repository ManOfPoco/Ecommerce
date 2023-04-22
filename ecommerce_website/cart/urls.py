from django.urls import path
from .views import (
    # CartView,
    CartListView,
    CartItemRemove,
    SaveForLaterCreate,
    MoveToCart,
    SaveForLaterRemove
)

app_name = 'cart'


urlpatterns = [
    path('', CartListView.as_view(), name='cart'),
    path('cart-item-remove/', CartItemRemove.as_view(), name='item-remove'),
    path('save-for-later-remove/', SaveForLaterRemove.as_view(), name='save-for-later-remove'),
    path('save-for-later/', SaveForLaterCreate.as_view(), name='save-for-later'),
    path('move-to-cart/', MoveToCart.as_view(), name='move-to-cart'),

]
