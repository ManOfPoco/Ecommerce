# Generated by Django 4.1.7 on 2023-04-07 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_attribute_attribute_value_delete_attributevalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Category Name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]