from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm

from .views import SignUpView, ProfileView, edit_profile


app_name = 'users'


urlpatterns = [
    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('sign-in', LoginView.as_view(template_name='registration/sign-in.html',
         authentication_form=UserLoginForm), name='sign-in'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit-profile/', edit_profile, name='edit-profile')
]
