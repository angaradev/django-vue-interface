# Generated by Django 3.0.2 on 2021-05-30 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_orderproducts_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='payment',
            field=models.CharField(choices=[('onGet', 'ПРИ ПОЛУЧЕНИИ'), ('onSite', 'ОНЛАЙН')], default='onGet', max_length=50),
        ),
    ]