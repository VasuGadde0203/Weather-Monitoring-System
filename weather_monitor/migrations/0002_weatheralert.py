# Generated by Django 5.1.2 on 2024-10-26 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(max_length=100)),
                ('temperature', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
