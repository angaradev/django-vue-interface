# Generated by Django 3.0.2 on 2020-11-05 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_category', '0016_auto_20201105_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engine',
            name='fuel',
            field=models.CharField(choices=[(0, 'Desel'), (1, 'Gasoline')], default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='engine',
            name='volume',
            field=models.CharField(choices=[(0, '3.0'), (1, '3.5'), (2, '2.5'), (3, '2.0'), (4, '1.5')], default=2, max_length=10),
        ),
    ]
