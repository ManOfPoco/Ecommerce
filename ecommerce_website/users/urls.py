from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

from .views import (
    SignUpView,
    CustomLoginView,
    ProfileView,
    edit_profile,
    OrderListView,
    OrderDetailView
)

app_name = 'users'


urlpatterns = [
    path('', RedirectView.as_view(url='/account/profile/')),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit-profile/', edit_profile, name='edit-profile'),

    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
]
