# Generated by Django 3.0.2 on 2021-03-16 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0064_auto_20210315_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='bages',
        ),
        migrations.AddField(
            model_name='productbages',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='product.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='productbages',
            unique_together={('name', 'product')},
        ),
    ]