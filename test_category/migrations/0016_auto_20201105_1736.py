# Generated by Django 3.0.2 on 2020-11-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_category', '0015_auto_20201105_1712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'verbose_name': 'Автомобил', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.AddField(
            model_name='engine',
            name='fuel',
            field=models.CharField(choices=[(0, 'Desel'), (1, 'Gasoline')], default='Desel', max_length=10),
        ),
        migrations.AddField(
            model_name='engine',
            name='volume',
            field=models.CharField(choices=[(0, '3.0'), (1, '3.5'), (2, '2.5'), (3, '2.0'), (4, '1.5')], default='2.5', max_length=10),
        ),
    ]
