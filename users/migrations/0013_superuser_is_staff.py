# Generated by Django 3.1.6 on 2021-05-11 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210512_0345'),
    ]

    operations = [
        migrations.AddField(
            model_name='superuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]