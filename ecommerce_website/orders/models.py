from django.db import models, transaction

from django.contrib.auth.models import User
from products.models import Product
from shippings.models import Shipping

from django.utils.translation import gettext_lazy as _


class OrderManager(models.Manager):

    @transaction.atomic
    def create_order(self, request, order_data):
        user = request.user if request.user.is_authenticated else None
        total_price = order_data['purchase_units'][0]['payments']['captures'][0]['amount']['value']
        order_status = OrderStatus.objects.get(status_name='Processing')
        items = request.session.get('order_data')

        order = Order.objects.create(
            user=user, total_price=total_price, order_status=order_status)
        products = []
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            product.quantity -= int(item['quantity'])
            product.save()
            products.append(
                OrderItem(order=order,
                          product=product,
                          price=item['price'],
                          quantity=item['quantity']
                          )
            )
        OrderItem.objects.bulk_create(products)
        del request.session['order_data']


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='order', null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.OneToOneField(
        Shipping, on_delete=models.CASCADE, null=True, blank=True)
    order_status = models.ForeignKey(
        'OrderStatus', on_delete=models.CASCADE, related_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    order_delivery_date = models.DateTimeField(auto_now=True)
    shipping_history = models.JSONField(default=list)
    status_history = models.JSONField(default=list)

    objects = OrderManager()

    def __str__(self) -> str:
        return f"{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='order_item')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.product.product_name}"


class OrderStatus(models.Model):
    status_name = models.CharField(_('Status Name'), max_length=100)

    class Meta:
        verbose_name_plural = 'Order Statuses'

    def __str__(self) -> str:
        return f"{self.status_name}"
