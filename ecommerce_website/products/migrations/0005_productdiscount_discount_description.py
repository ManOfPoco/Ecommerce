# Generated by Django 4.1.7 on 2023-04-06 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdiscount',
            name='discount_description',
            field=models.TextField(default='', verbose_name='Discount Description'),
            preserve_default=False,
        ),
    ]