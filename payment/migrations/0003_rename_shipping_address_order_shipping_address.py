# Generated by Django 5.1 on 2024-09-07 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_order_orderitems'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Shipping_address',
            new_name='shipping_address',
        ),
    ]
