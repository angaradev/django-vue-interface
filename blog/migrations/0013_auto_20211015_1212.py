# Generated by Django 3.0.2 on 2021-10-15 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(default='Team of PartsHub.ru', max_length=100),
        ),
    ]