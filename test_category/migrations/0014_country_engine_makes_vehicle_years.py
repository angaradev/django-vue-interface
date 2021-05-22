# Generated by Django 3.0.2 on 2020-11-05 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_category', '0013_categories_layout'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Страна',
            },
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Двигатель',
            },
        ),
        migrations.CreateModel(
            name='Makes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='test_category.Country')),
            ],
            options={
                'verbose_name': 'Марка',
            },
        ),
        migrations.CreateModel(
            name='Years',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Год',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('engine', models.CharField(max_length=255)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='test_category.Makes')),
                ('year_from', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='year_from', to='test_category.Years')),
                ('year_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='year_to', to='test_category.Years')),
            ],
            options={
                'verbose_name': 'Автомобили',
            },
        ),
    ]
