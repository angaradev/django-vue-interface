# Generated by Django 3.0.2 on 2021-04-24 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_post_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='priority',
            field=models.IntegerField(blank=True, choices=[(5, 'Higest'), (4, 'High'), (3, 'Medium'), (2, 'Low'), (1, 'Lowest')], default=1, null=True),
        ),
    ]