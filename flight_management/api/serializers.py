from django.utils import timezone
from rest_framework import serializers

from api.models import Aircraft, Flight, Airport


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ('serial_number', 'manufacturer')
        read_only_fields = ()


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('id', 'aircraft',
                  'departure_airport', 'depart_at',
                  'arrival_airport', 'arrive_at')

    def validate(self, attrs):
        if attrs['depart_at'] < timezone.now():
            raise serializers.ValidationError({"depart_at": "depart date must occur in future"})
        if attrs['depart_at'] > attrs['arrive_at']:
            raise serializers.ValidationError({"arrive_at": "arrive date must occur after depart"})
        return attrs


class CreateFlightSerializer(FlightSerializer):
    class Meta:
        model = Flight
        fields = ('id', 'aircraft',
                  'departure_airport', 'depart_at',
                  'arrival_airport', 'arrive_at')


class UpdateFlightSerializer(FlightSerializer):
    class Meta:
        model = Flight
        fields = ('id', 'departure_airport', 'depart_at',
                  'arrival_airport', 'arrive_at')


class MinutesDurationField(serializers.DurationField):
    def to_representation(self, value):
        return value.total_seconds() / 60


class InFlightSerializer(serializers.ModelSerializer):
    in_flight_minutes = MinutesDurationField()

    class Meta:
        model = Flight
        fields = ('id', 'aircraft',
                  'departure_airport', 'depart_at',
                  'arrival_airport', 'arrive_at',
                  'in_flight_minutes')


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('icao', 'name')


class AirportInFlightSerializer(serializers.ModelSerializer):
    in_flight_count = serializers.IntegerField()
    departure_flights = InFlightSerializer(many=True)

    class Meta:
        model = Airport
        fields = ('icao', 'name', 'departure_flights', 'in_flight_count')
