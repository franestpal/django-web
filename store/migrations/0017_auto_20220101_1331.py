# Generated by Django 3.1.7 on 2022-01-01 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_item_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
    ]