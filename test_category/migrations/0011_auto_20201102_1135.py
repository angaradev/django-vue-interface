# Generated by Django 3.0.2 on 2020-11-02 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_category', '0010_auto_20201102_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producttwo',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='producttwo',
            name='categories',
        ),
        migrations.DeleteModel(
            name='CategoriesTree',
        ),
        migrations.DeleteModel(
            name='ProductTwo',
        ),
    ]