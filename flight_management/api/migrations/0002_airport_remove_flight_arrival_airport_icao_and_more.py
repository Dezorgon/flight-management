# Generated by Django 4.1.7 on 2023-02-24 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('icao', models.CharField(max_length=4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='flight',
            name='arrival_airport_icao',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='departure_airport_icao',
        ),
        migrations.AddField(
            model_name='flight',
            name='arrival_airport',
            field=models.ForeignKey(
                default='',
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='arrival_flights',
                to='api.airport',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flight',
            name='departure_airport',
            field=models.ForeignKey(
                default='',
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='departure_flights',
                to='api.airport',
            ),
            preserve_default=False,
        ),
    ]
