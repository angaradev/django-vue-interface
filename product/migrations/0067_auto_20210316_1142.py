# Generated by Django 3.0.2 on 2021-03-16 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0066_auto_20210316_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbages',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bages', to='product.Product'),
        ),
    ]
