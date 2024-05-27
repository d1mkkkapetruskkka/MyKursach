# Generated by Django 4.2.7 on 2024-05-26 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_payment_on_get_alter_order_price_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price_model',
            field=models.CharField(choices=[('CPC', 'За количество щелчков мышью(СPC)'), ('CPM', 'За количество показов(CPM)'), ('CPA', 'За количество действий(CPA)')], max_length=3, verbose_name='Выбор ценовой модели'),
        ),
    ]