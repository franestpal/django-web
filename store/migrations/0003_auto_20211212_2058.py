# Generated by Django 3.1.7 on 2021-12-12 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20211212_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='discount_price',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]