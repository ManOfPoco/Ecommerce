from django.urls import path
from .views import payment_done, payment_canceled

app_name = 'paypal'


urlpatterns = [
    path('payment/done/', payment_done, name='payment-done'),
    path('payment/canceled/', payment_canceled, name='payment-canceled'),
]
