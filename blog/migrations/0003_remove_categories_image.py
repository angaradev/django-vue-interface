# Generated by Django 3.0.2 on 2020-10-18 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20201017_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='image',
        ),
    ]