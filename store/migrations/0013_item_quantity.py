# Generated by Django 3.1.7 on 2022-01-01 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20211225_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
