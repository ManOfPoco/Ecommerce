# Generated by Django 4.2 on 2023-04-19 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_brand_brand_name_alter_brand_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productdiscount',
            old_name='manimum_order_value',
            new_name='minimum_order_value',
        ),
    ]