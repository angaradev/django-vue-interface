# Generated by Django 3.0.2 on 2021-10-15 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0094_category_cat_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='cat_banner',
        ),
    ]