# Generated by Django 3.1.6 on 2021-05-19 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0003_auto_20210419_1418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buses',
            old_name='tprice',
            new_name='total_price',
        ),
    ]
