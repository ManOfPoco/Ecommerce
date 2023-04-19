from django import template
from decimal import Decimal
from django.utils.safestring import SafeString

register = template.Library()


@register.simple_tag
def calculate_discount_saving(regular_price: Decimal, discount_price: Decimal):
    discount_sum = round(regular_price, 2) - round(discount_price, 2)
    discount_percent = round(discount_sum / regular_price * 100)

    return f"${discount_sum} ({discount_percent}%)"


@register.simple_tag
def build_url_path(category):
    category_ancestors = category.get_ancestors(include_self=True)
    path = '/'.join([category.slug for category in category_ancestors])

    return path


@register.filter
def is_string(value):
    return isinstance(value, SafeString)


@register.filter
def get_dict_value(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def make_int_list(num: str):
    return [i for i in range(1, int(num) + 1)]
