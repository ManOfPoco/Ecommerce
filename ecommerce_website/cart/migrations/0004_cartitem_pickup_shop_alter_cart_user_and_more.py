# Generated by Django 4.2 on 2023-04-19 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0001_initial'),
        ('cart', '0003_cartitem_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='pickup_shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='ecommerce.shop'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.UniqueConstraint(fields=('product', 'cart'), name='unique_product_in_cart', violation_error_message="Cart can't have the same products"),
        ),
        migrations.AddConstraint(
            model_name='saveforlater',
            constraint=models.UniqueConstraint(fields=('product', 'cart'), name='unique_product_in_save_for_later', violation_error_message="Save For Later can't have the same products"),
        ),
    ]
