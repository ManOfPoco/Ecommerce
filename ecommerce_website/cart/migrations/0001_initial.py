# Generated by Django 4.2 on 2023-06-17 15:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ecommerce', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='SaveForLater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='save_for_later', to='cart.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='save_for_later', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.cart')),
                ('pickup_shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='ecommerce.shop')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='products.product')),
            ],
        ),
        migrations.AddConstraint(
            model_name='saveforlater',
            constraint=models.UniqueConstraint(fields=('product', 'cart'), name='unique_product_in_save_for_later', violation_error_message="Save For Later can't have the same products"),
        ),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.UniqueConstraint(fields=('product', 'cart'), name='unique_product_in_cart', violation_error_message="Cart can't have the same products"),
        ),
    ]
