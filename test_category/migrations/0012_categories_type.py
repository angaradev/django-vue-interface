# Generated by Django 3.0.2 on 2020-11-02 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_category', '0011_auto_20201102_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='type',
            field=models.CharField(default='shop', max_length=30),
        ),
    ]