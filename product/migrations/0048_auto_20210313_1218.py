# Generated by Django 3.0.2 on 2021-03-13 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0047_auto_20210313_1211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='layout',
            new_name='layout_test',
        ),
    ]
