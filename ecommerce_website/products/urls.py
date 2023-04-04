from django.urls import path
from django.views.generic import RedirectView
from .views import CategoryView


app_name = 'products'


urlpatterns = [
    path('', RedirectView.as_view(url='/')),
    path('<slug:slug>/', CategoryView.as_view(), name='category'),
]
