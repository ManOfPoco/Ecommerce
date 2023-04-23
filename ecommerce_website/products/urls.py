from django.urls import path
from django.views.generic import RedirectView
from .views import CategoryView, products_list, ProductDetailView


app_name = 'products'


urlpatterns = [
    path('', RedirectView.as_view(url='/')),
    path('<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug:product_slug>/',
         ProductDetailView.as_view(), name='product-overview'),

    path('<path:category_path>/', products_list, name='all-products'),
]
