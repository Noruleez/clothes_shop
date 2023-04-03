# Generated by Django 4.1.7 on 2023-04-01 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_order_options_order_status_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_address', models.CharField(max_length=50, verbose_name='адрес доставки')),
                ('delivery_period', models.DateTimeField(verbose_name='время доставки')),
                ('payment_status', models.CharField(max_length=50, verbose_name='статус оплаты')),
                ('delivery_status', models.CharField(max_length=50, verbose_name='статус доставки')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_order', to='products.order', verbose_name='заказ')),
            ],
        ),
    ]