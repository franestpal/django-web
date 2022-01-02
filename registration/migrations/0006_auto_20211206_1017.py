# Generated by Django 3.1.7 on 2021-12-06 10:17

from django.db import migrations, models
import registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20211205_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=registration.models.custom_upload_to),
        ),
    ]
