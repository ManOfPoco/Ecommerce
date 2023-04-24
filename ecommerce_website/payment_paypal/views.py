from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payment_done(request):
    return render(request, 'payment_paypal/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_paypal/payment_canceled.html')
