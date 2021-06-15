# Generated by Django 3.0.2 on 2021-05-30 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20210528_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproducts',
            name='product_image',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='product_slug',
            field=models.SlugField(default='change_me', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='delivery',
            field=models.CharField(choices=[('self', 'САМОВЫВОЗ'), ('kur', 'КУРЬЕРОМ'), ('poset', 'ТРАНСПОРТНОЙ КОМПАНИЕЙ')], default='self', max_length=50),
        ),
        migrations.AddField(
            model_name='orders',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='payment',
            field=models.CharField(choices=[('OnGet', 'ПРИ ПОЛУЧЕНИИ'), ('OnSite', 'ОНЛАЙН')], default='OnGet', max_length=50),
        ),
        migrations.AddField(
            model_name='orders',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='total_front',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
    ]