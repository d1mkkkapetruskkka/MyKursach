# Generated by Django 4.2.7 on 2024-05-25 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_payment_on_get'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_on_get',
            field=models.BooleanField(default=False, verbose_name='Способ оплаты'),
        ),
    ]
