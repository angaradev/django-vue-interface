# Generated by Django 3.0.2 on 2021-03-15 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0054_auto_20210315_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmake',
            name='priority',
            field=models.CharField(choices=[('HIGEST', 'HIGEST'), ('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW'), ('LOWEST', 'LOWEST')], default='LOWEST', max_length=100),
        ),
    ]
