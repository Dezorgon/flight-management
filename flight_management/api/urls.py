from rest_framework_nested import routers

from api.views import AircraftViewSet, ReadFlightPageViewSet, FlightPageViewSet, AirportViewSet

router = routers.SimpleRouter()

router.register(r'airports', AirportViewSet)

router.register(r'aircraft', AircraftViewSet)
aircraft_router = routers.NestedSimpleRouter(router, 'aircraft', lookup='aircraft')
aircraft_router.register('flights', ReadFlightPageViewSet)

router.register(r'flights', FlightPageViewSet)

urlpatterns = [
] + router.urls + aircraft_router.urls
