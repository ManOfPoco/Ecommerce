from django.urls import path
from django.views.generic import RedirectView
from .views import CategoryView, category_products


app_name = 'products'


urlpatterns = [
    path('', RedirectView.as_view(url='/')),
    path('<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('<path:category_path>/', category_products, name='products'),
]
