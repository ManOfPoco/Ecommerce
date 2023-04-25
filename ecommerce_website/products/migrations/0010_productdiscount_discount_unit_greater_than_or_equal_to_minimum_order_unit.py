# Generated by Django 4.2 on 2023-04-23 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_manimum_order_value_productdiscount_minimum_order_value'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='productdiscount',
            constraint=models.CheckConstraint(check=models.Q(('discount_unit__gte', models.F('minimum_order_value'))), name='discount_unit_greater_than_or_equal_to_minimum_order_unit', violation_error_message='Discount unit should be greater or equal to the minimum order value'),
        ),
    ]