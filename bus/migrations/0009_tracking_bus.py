# Generated by Django 3.1.6 on 2021-06-15 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0008_auto_20210615_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracking',
            name='bus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bus.buses'),
        ),
    ]
