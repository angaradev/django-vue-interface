# Generated by Django 3.0.2 on 2020-03-12 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20200312_2121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='url',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='productimage',
            old_name='img',
            new_name='product',
        ),
    ]
