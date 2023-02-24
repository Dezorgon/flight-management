from django_filters import DateTimeFilter, FilterSet

from api.models import Airport, Flight


class AirportFilter(FilterSet):
    date_from = DateTimeFilter(field_name="departure_flights__arrive_at", lookup_expr="gt")
    date_to = DateTimeFilter(field_name="departure_flights__depart_at", lookup_expr="lt")

    class Meta:
        model = Airport
        fields = [
            "icao",
            "name",
            "date_from",
            "date_to",
        ]


class FlightFilter(FilterSet):
    depart_from = DateTimeFilter(field_name="depart_at", lookup_expr="gte")
    depart_to = DateTimeFilter(field_name="depart_at", lookup_expr="lte")

    class Meta:
        model = Flight
        fields = [
            "departure_airport__icao",
            "depart_at",
            "arrival_airport__icao",
            "arrive_at",
        ]
