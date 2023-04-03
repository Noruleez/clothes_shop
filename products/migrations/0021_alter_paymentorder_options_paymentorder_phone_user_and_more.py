# Generated by Django 4.1.7 on 2023-04-01 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_paymentorder'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentorder',
            options={'verbose_name': 'заказ для оплаты', 'verbose_name_plural': 'Заказы с оплатой'},
        ),
        migrations.AddField(
            model_name='paymentorder',
            name='phone_user',
            field=models.CharField(default=1, max_length=50, verbose_name='время доставки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentorder',
            name='delivery_period',
            field=models.CharField(max_length=50, verbose_name='время доставки'),
        ),
    ]
