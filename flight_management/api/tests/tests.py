from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from api import services
from api.tests.factories import AirportFactory, FlightFactory


@pytest.mark.django_db
def test_get_airports_with_all_flights():
    batch_count = 10
    departure_airport = AirportFactory()
    FlightFactory.create_batch(batch_count, departure_airport=departure_airport)
    airports = services.airport.get_airports_with_departure_flights(
        date_from=datetime.min,
        date_to=datetime.max,
    )
    airport = airports.get(icao=departure_airport.icao)

    assert len(airport.departure_flights.all()) == batch_count


@pytest.mark.django_db
def test_get_airport_with_partial_flight():
    depart_at = timezone.datetime(year=2020, month=1, day=1, hour=1)
    arrive_at = timezone.datetime(year=2020, month=1, day=1, hour=3)

    airport = AirportFactory()
    FlightFactory(
        depart_at=depart_at,
        arrive_at=arrive_at,
        departure_airport=airport,
        arrival_airport=airport,
    )

    airports = services.airport.get_airports_with_departure_flights(
        date_from=depart_at + timedelta(hours=1),
        date_to=arrive_at,
    )

    assert len(airports) == 1
    assert len(airports[0].departure_flights.all()) == 1
    assert airports[0].in_flight_count == 1

    in_flight_time = arrive_at - (depart_at + timedelta(hours=1))
    assert airports[0].departure_flights.all()[0].in_flight_minutes == in_flight_time


@pytest.mark.django_db
def test_airports_list_200(client):
    batch_count = 10
    FlightFactory.create_batch(batch_count)

    url = reverse('airport-list')
    response = client.get(url)
    data = response.json()["results"]

    assert response.status_code == 200
    assert len(data) == batch_count * 2
