from django.urls import path
from django.views.generic import RedirectView
from .views import CategoryView, ProductView, ProductsView


app_name = 'products'


urlpatterns = [
    path('', RedirectView.as_view(url='/')),
    path('<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug:product_slug>/',
         ProductView.as_view(), name='product-overview'),

    path('<path:category_path>/', ProductsView.as_view(), name='all-products'),
]
