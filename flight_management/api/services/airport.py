from datetime import datetime

from django.db import models
from django.db.models import Count, F, Prefetch, Q
from django.db.models.functions import Greatest, Least

from api.models import Airport, Flight


def _annotate_in_flight_count(
    queryset: models.QuerySet,
    *,
    date_from: datetime,
    date_to: datetime,
) -> models.QuerySet:
    return queryset.annotate(
        in_flight_count=Count(
            'departure_flights',
            filter=Q(departure_flights__arrive_at__gt=date_from, departure_flights__depart_at__lt=date_to),
            distinct=True,
        )
    )


def _prefetch_partial_flights(
    queryset: models.QuerySet,
    *,
    date_from: datetime,
    date_to: datetime,
) -> models.QuerySet:
    return queryset.prefetch_related(
        Prefetch(
            "departure_flights",
            Flight.objects.annotate(
                in_flight_minutes=Least(F('arrive_at'), date_to) - Greatest(F('depart_at'), date_from)
            ).filter(arrive_at__gt=date_from, depart_at__lt=date_to),
        )
    )


def get_airports_with_departure_flights(
    *,
    date_from: datetime,
    date_to: datetime,
) -> models.QuerySet:
    queryset = Airport.objects.all()
    queryset = _annotate_in_flight_count(
        queryset,
        date_from=date_from,
        date_to=date_to,
    )
    queryset = _prefetch_partial_flights(
        queryset,
        date_from=date_from,
        date_to=date_to,
    )
    return queryset.all()
