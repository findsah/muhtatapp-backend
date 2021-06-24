# Generated by Django 3.1.6 on 2021-06-15 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0006_tracking'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buses',
            options={'verbose_name': 'Bus', 'verbose_name_plural': 'Buses'},
        ),
        migrations.AlterModelOptions(
            name='busstation',
            options={'verbose_name': 'Bus Station', 'verbose_name_plural': 'Bus Stations'},
        ),
        migrations.AlterModelOptions(
            name='seats',
            options={'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
        migrations.AlterField(
            model_name='seats',
            name='seat_number',
            field=models.IntegerField(verbose_name='Ticket Number'),
        ),
        migrations.CreateModel(
            name='P_Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pass_count', models.IntegerField(max_length=300)),
                ('date_time', models.IntegerField()),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.buses')),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField()),
                ('filename', models.CharField(max_length=500)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.buses')),
            ],
        ),
    ]