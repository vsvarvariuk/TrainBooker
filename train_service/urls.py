from rest_framework import routers
from django.urls import path, include
from train_service.views import (TrainViewSet,
                                TrainTypeViewSet,
                                CrewViewSet,
                                StationViewSet,
                                RouteViewSet,
                                JourneyViewSet,
                                OrderViewSet,
                                CityViewSet)

router = routers.DefaultRouter()
router.register("type-trains", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("crews", CrewViewSet)
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("journeys", JourneyViewSet)
router.register("orders", OrderViewSet)
router.register("cities", CityViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "ticket_train"