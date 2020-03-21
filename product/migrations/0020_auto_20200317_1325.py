# Generated by Django 3.0.2 on 2020-03-17 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0006_auto_20200312_1703'),
        ('product', '0019_auto_20200316_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='name',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_brand', to='brands.BrandsDict'),
        ),
    ]
