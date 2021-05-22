# Generated by Django 3.0.2 on 2021-04-18 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_auto_20210418_1025"),
        ("product", "0082_auto_20210418_1045"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productrating",
            name="autoUser",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="autouser_rating",
                to="users.AutoUser",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="productrating",
            unique_together={("product", "autoUser")},
        ),
    ]
