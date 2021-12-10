# Generated by Django 3.0.2 on 2021-12-10 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0105_auto_20211103_1737'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['cat_number', 'name', 'slug'], name='product_pro_cat_num_277863_idx'),
        ),
    ]
