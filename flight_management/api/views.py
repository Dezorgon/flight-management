from datetime import datetime

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from utils.view_mixins import GetSerializerMixin

from api import services
from api.filtersets import AirportFilter, FlightFilter
from api.models import Aircraft, Airport, Flight
from api.serializers import (
    AircraftSerializer,
    AirportInFlightSerializer,
    AirportSerializer,
    FlightSerializer,
    UpdateFlightSerializer,
)


class AirportViewSet(GetSerializerMixin, ModelViewSet):
    queryset = Airport.objects.all()
    serializer_classes = {
        'list': AirportInFlightSerializer,
        'default': AirportSerializer,
    }

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = AirportFilter
    search_fields = ('icao',)
    ordering_fields = ('icao',)

    def get_queryset(self):
        if self.action == 'list':
            form = AirportFilter().get_form_class()(self.request.query_params)
            form.is_valid()

            date_from = form.cleaned_data.get("date_from") or datetime.min
            date_to = form.cleaned_data.get("date_to") or datetime.max

            return services.airport.get_airports_with_departure_flights(
                date_from=date_from,
                date_to=date_to,
            )

        return self.queryset


class AircraftViewSet(GetSerializerMixin, ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_classes = {
        'default': AircraftSerializer,
    }

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('serial_number', 'manufacturer')
    ordering_fields = ('serial_number',)


class ReadFlightPageViewSet(GetSerializerMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Flight.objects.all()
    serializer_classes = {
        'default': FlightSerializer,
    }

    def get_queryset(self):
        serial_number = self.kwargs.get('aircraft_pk')
        aircraft = get_object_or_404(Aircraft, pk=serial_number)

        if self.action == 'list':
            return self.queryset.filter(aircraft=aircraft)

        return self.queryset


class FlightPageViewSet(GetSerializerMixin, ModelViewSet):
    queryset = Flight.objects.all()
    serializer_classes = {
        'create': FlightSerializer,
        'update': UpdateFlightSerializer,
        'partial_update': UpdateFlightSerializer,
        'default': FlightSerializer,
    }

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = FlightFilter
    search_fields = ('departure_airport_icao', 'arrival_airport_icao')
    ordering_fields = ("depart_at", "arrive_at")
