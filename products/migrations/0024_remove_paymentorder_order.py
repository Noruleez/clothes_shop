# Generated by Django 4.1.7 on 2023-04-01 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_paymentorder_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentorder',
            name='order',
        ),
    ]
