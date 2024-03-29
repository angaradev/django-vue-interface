# Generated by Django 3.0.2 on 2021-02-12 08:39

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0046_auto_20201028_0925"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="layout",
            field=models.CharField(default="products", max_length=30),
        ),
        migrations.AddField(
            model_name="category",
            name="type",
            field=models.CharField(default="shop", max_length=30),
        ),
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="children",
                to="product.Category",
            ),
        ),
        migrations.CreateModel(
            name="Categories",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("type", models.CharField(default="shop", max_length=30)),
                ("layout", models.CharField(default="products", max_length=30)),
                ("slug", models.SlugField(blank=True)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="children",
                        to="product.Categories",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категории",
            },
        ),
    ]
