# Generated by Django 3.0.2 on 2021-10-15 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0093_category_cat_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_banner',
            field=models.ImageField(blank=True, help_text='Banner for site pages dimension must be 5:1', null=True, upload_to='images/categories'),
        ),
    ]