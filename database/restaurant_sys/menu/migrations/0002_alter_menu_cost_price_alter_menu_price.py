# Generated by Django 4.2.5 on 2024-01-02 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='cost_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.FloatField(),
        ),
    ]
