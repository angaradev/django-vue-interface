# Generated by Django 3.0.2 on 2021-10-15 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0092_auto_20210802_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/categories'),
        ),
    ]