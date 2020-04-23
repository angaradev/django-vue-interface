# Generated by Django 3.0.2 on 2020-03-25 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_auto_20200324_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='AngaraOld',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('car_model', models.IntegerField()),
                ('one_c_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='carmake',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='car_model', to='product.CarMake'),
        ),
        migrations.AlterField(
            model_name='product',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='model_product', to='product.CarModel'),
        ),
    ]