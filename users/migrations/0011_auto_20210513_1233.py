# Generated by Django 3.0.2 on 2021-05-13 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20210513_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useradresses',
            name='autouser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address_autouser', to='users.AutoUser'),
        ),
        migrations.AlterField(
            model_name='useradresses',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
