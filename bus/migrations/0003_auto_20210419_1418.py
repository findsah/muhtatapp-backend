# Generated by Django 3.1.6 on 2021-04-19 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0002_buses_destination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buses',
            name='destination',
            field=models.CharField(default='Ferozepur', max_length=500),
        ),
    ]
