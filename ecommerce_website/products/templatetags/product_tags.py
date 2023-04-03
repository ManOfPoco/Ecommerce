from django import template
from decimal import Decimal

register = template.Library()


@register.simple_tag
def calculate_discount_saving(regular_price: Decimal, discount_price: Decimal):
    discount_sum = round(regular_price, 2) - round(discount_price, 2)
    discount_percent = discount_sum / 100 * 100

    return f"${discount_sum} ({round(discount_percent)}%)"
