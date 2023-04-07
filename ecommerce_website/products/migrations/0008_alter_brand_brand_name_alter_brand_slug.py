# Generated by Django 4.1.7 on 2023-04-07 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_category_category_name_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='brand_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Brand Name'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
