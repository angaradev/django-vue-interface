# Generated by Django 3.0.2 on 2021-05-28 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210528_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproducts',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
    ]
