from django.contrib import admin

from .models import Order, OrderItem, OrderStatus

admin.site.register((Order, OrderItem, OrderStatus))
