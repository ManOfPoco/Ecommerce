from django.shortcuts import redirect
from django.urls import reverse

from .forms import MyPayPalPaymentsForm

from django.conf import settings

from uuid import uuid4


def create_payment_form(request, item_number, total_price):

    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'item_name': 'Big Lots Payment',
        'amount': str(round(total_price, 2)),
        'item_number': str(item_number),
        'invoice': str(uuid4()),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('cart:cart')}",
        'return_url': f"http://{host}{reverse('paypal:payment-done')}",
        'cancel_return': f"http://{host}{reverse('paypal:payment-canceled')}",
    }

    form = MyPayPalPaymentsForm(initial=paypal_dict)

    return form
