from django.shortcuts import render
from django.http import JsonResponse

from django.conf import settings

from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

from cart.models import Cart, CartItem

from django.views.generic import TemplateView
from cart.mixins import CartItemsCountMixin

from orders.models import Order

from django.db import transaction


class PaymentDoneView(CartItemsCountMixin, TemplateView):
    template_name = 'payment_paypal/payment_done.html'


class PaymentCanceledView(CartItemsCountMixin, TemplateView):
    template_name = 'payment_paypal/payment_canceled.html'


def pay(request):
    client_id = settings.PAYPAL_CLIENT_ID
    return render(request, 'pay.html', context={'client_id': client_id})


@transaction.atomic
def create_payment_order(request):
    if request.method == "POST":

        environment = SandboxEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_ID)
        client = PayPalHttpClient(environment)

        cart = Cart.objects.get_or_create_cart(request=request)
        queryset = CartItem.objects.get_cart_products(cart=cart)
        bill = CartItem.objects.calculate_bill(queryset=queryset)

        items, order_data = [], []
        for item in queryset:
            order_data.append({
                'product_id': str(item.product.id),
                'price': str(item.current_price),
                'quantity': str(item.quantity)
            })
            items.append(
                {
                    "name": item.product.product_name,
                    "sku": str(item.product.sku),
                    "unit_amount": {
                        "currency_code": "USD",
                        "value": str(item.current_price / item.quantity)
                    },
                    "quantity": str(item.quantity),
                },
            )

        request.session['order_data'] = order_data
        # order
        create_order = OrdersCreateRequest()
        create_order.request_body(
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "description": "Big Lots Goods",
                        "amount": {
                            "currency_code": "USD",
                            "value": str(bill.get('total_price')),
                            "breakdown": {
                                "item_total": {
                                    "currency_code": "USD",
                                    "value": str(bill.get('total_price'))
                                }
                            },
                        },
                        "items": [
                            *items
                        ],

                    }
                ]
            }
        )

        response = client.execute(create_order)
        data = response.result.__dict__['_dict']

        return JsonResponse(data)
    else:
        return JsonResponse({'details': "invalide request"})


@transaction.atomic
def capture_payment_order(request, order_id):
    if request.method == "POST":
        capture_order = OrdersCaptureRequest(order_id)
        environment = SandboxEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_ID)
        client = PayPalHttpClient(environment)

        response = client.execute(capture_order)
        data = response.result.__dict__['_dict']

        print(response.result)
        print(data)
        Order.objects.create_order(request=request, order_data=data)
        return JsonResponse(data)
    else:
        return JsonResponse({'details': "invalide request"})
