# Generated by Django 3.1.7 on 2022-01-01 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_item_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
    ]