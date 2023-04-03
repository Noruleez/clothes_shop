# Generated by Django 4.1.7 on 2023-03-20 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_order_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'заказ', 'verbose_name_plural': 'Заказы пользователей'},
        ),
        migrations.AddField(
            model_name='order',
            name='status_payment',
            field=models.CharField(default='Не оплачено', max_length=50),
        ),
    ]
