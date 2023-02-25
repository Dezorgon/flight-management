import factory
from django.utils import timezone

from api.models import Aircraft, Airport, Flight


class AircraftFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Aircraft

    serial_number = factory.Faker('random_number', digits=6)


class AirportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Airport

    icao = factory.Faker('random_number', digits=4)


class FlightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Flight

    depart_at = factory.Faker(
        'date_time_between',
        start_date=timezone.now(),
    )
    arrive_at = factory.Faker(
        'date_time_between',
        end_date=factory.SelfAttribute('..depart_at'),
    )
    aircraft = factory.SubFactory(AircraftFactory)
    departure_airport = factory.SubFactory(AirportFactory)
    arrival_airport = factory.SubFactory(AirportFactory)
