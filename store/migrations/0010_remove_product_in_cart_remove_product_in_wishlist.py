# Generated by Django 5.1.6 on 2025-02-21 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_delete_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='in_cart',
        ),
        migrations.RemoveField(
            model_name='product',
            name='in_wishlist',
        ),
    ]
