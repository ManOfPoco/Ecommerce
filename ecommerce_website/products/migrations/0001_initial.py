# Generated by Django 4.2 on 2023-06-17 15:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shippings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_name', models.CharField(max_length=255, verbose_name='Attribute Name')),
                ('attribute_value', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Attributes',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=255, unique=True, verbose_name='Brand Name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='brands')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('image', models.ImageField(max_length=255, upload_to='categories')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='products.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_name', models.CharField(max_length=100, unique=True, verbose_name='Collection Name')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, verbose_name='Coupon Code')),
                ('coupon_description', models.TextField(blank=True, null=True, verbose_name='Coupon Description')),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_type', models.CharField(max_length=50, verbose_name='Discount Type')),
                ('max_usage', models.IntegerField()),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('expire_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_description', models.TextField(verbose_name='Feature Description')),
            ],
            options={
                'verbose_name_plural': 'Features',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('regular_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sku', models.IntegerField(unique=True)),
                ('slug', models.SlugField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attribute', models.ManyToManyField(blank=True, to='products.attribute')),
                ('available_shipping_types', models.ManyToManyField(blank=True, to='shippings.shippingtype')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', to='products.brand')),
                ('category', models.ManyToManyField(to='products.category')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', to='products.collection')),
                ('coupon', models.ManyToManyField(blank=True, to='products.coupon')),
                ('features', models.ManyToManyField(blank=True, to='products.features')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.ImageField(upload_to='products')),
                ('alternative_text', models.CharField(blank=True, max_length=50, null=True)),
                ('is_default', models.BooleanField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_description', models.TextField(verbose_name='Discount Description')),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_unit', models.IntegerField()),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('expire_date', models.DateTimeField(blank=True, null=True)),
                ('minimum_order_value', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('maximum_order_value', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='products.product')),
            ],
        ),
        migrations.AddConstraint(
            model_name='productdiscount',
            constraint=models.CheckConstraint(check=models.Q(('discount_unit__gte', models.F('minimum_order_value'))), name='discount_unit_greater_than_or_equal_to_minimum_order_unit', violation_error_message='Discount unit should be greater or equal to the minimum order value'),
        ),
    ]
