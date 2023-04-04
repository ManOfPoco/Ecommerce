from django import template
from decimal import Decimal
from django.utils.safestring import SafeString

register = template.Library()


@register.simple_tag
def calculate_discount_saving(regular_price: Decimal, discount_price: Decimal):
    discount_sum = round(regular_price, 2) - round(discount_price, 2)
    discount_percent = round(discount_sum / 100 * 100)

    return f"${discount_sum} ({discount_percent}%)"


@register.filter
def if_string(value):
    return isinstance(value, SafeString)


@register.filter
def get_dict_value(dictionary, key):
    return dictionary.get(key)
