# Generated by Django 4.2.7 on 2024-05-21 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price_model',
            field=models.BooleanField(default=False, verbose_name='Выбор ценовой модели'),
        ),
    ]
