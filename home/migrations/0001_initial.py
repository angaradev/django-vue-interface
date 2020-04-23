# Generated by Django 3.0.2 on 2020-04-11 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Документация',
                'verbose_name_plural': 'Документация',
            },
        ),
    ]