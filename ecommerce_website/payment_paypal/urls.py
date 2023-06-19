from django.urls import path
from .views import pay, create_payment_order, capture_payment_order, PaymentDoneView, PaymentCanceledView

app_name = 'paypal'


urlpatterns = [
    path('paypal/pay/', pay, name="pay"),
    path('paypal/create/', create_payment_order, name="paypal-create"),
    path('paypal/<order_id>/capture/', capture_payment_order, name="paypal-capture"),
    path('paypal/done/', PaymentDoneView.as_view(), name='paypal-done'),
    path('paypal/canceled/', PaymentCanceledView.as_view(), name='paypal-canceled'),
]
