# Generated by Django 3.0.2 on 2021-03-16 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0068_carmodel_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='name',
            field=models.CharField(blank=True, max_length=45, unique=True),
        ),
    ]