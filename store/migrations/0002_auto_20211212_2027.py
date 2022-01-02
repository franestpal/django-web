# Generated by Django 3.1.7 on 2021-12-12 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Post_name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('discount_price', models.CharField(blank=True, max_length=20, null=True)),
                ('category', models.CharField(choices=[('P', 'Pescados'), ('M', 'Mariscos'), ('C', 'Conservas')], max_length=2)),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog', verbose_name='Imagen')),
            ],
        ),
        migrations.RenameField(
            model_name='order',
            old_name='items',
            new_name='Posts',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.post'),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]