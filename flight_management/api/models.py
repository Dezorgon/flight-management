from django.db import models


class Aircraft(models.Model):
    serial_number = models.CharField(
        max_length=30,
        unique=True,
        primary_key=True,
    )
    manufacturer = models.CharField(max_length=30)


class Airport(models.Model):
    icao = models.CharField(
        max_length=4,
        unique=True,
        primary_key=True,
    )
    name = models.CharField(max_length=64)


class Flight(models.Model):
    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.CASCADE,
        related_name='flights',
    )

    departure_airport = models.ForeignKey(
        Airport,
        on_delete=models.DO_NOTHING,
        related_name='departure_flights',
    )
    depart_at = models.DateTimeField()

    arrival_airport = models.ForeignKey(
        Airport,
        on_delete=models.DO_NOTHING,
        related_name='arrival_flights',
    )
    arrive_at = models.DateTimeField()

    class Meta:
        ordering = ('id',)
