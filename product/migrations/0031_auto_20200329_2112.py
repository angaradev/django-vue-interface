# Generated by Django 3.0.2 on 2020-03-29 18:12

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_auto_20200327_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=mptt.fields.TreeManyToManyField(blank=True, related_name='category_reverse', to='product.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='engine',
            field=models.ManyToManyField(blank=True, related_name='car_related_engine', to='product.CarEngine'),
        ),
    ]
