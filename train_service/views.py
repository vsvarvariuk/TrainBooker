from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from train_service.models import (TrainType,
                                 Train,
                                 Order,
                                 Crew,
                                 Journey,
                                 Route,
                                 Station,
                                 City)
from train_service.serializers import (TrainSerializer,
                                      TrainTypeSerializer,
                                      CrewSerializer,
                                      CitySerializer,
                                      StationSerializer,
                                      RouteSerializer,
                                      JourneySerializer,
                                      OrderSerializer,
                                      RouteDetailSerializer,
                                      StationCreateSerializer,
                                      JourneyListSerializer,
                                      JourneyDetailSerializer,
                                      OrderDetailSerializer,
                                      TrainCreateSerializer,
                                      RouteCreateSerializer,
                                      ImageSerializer)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    @action(methods=["POST"],
            detail=True,
            url_path="image")
    def upload_image(self, request, pk=None):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "create":
            return TrainCreateSerializer
        if self.action == "upload_image":
            return ImageSerializer
        return TrainSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def get_queryset(self):
        queryset = Station.objects.all().select_related("city")
        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__name__icontains=city)
            return queryset
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "city",
                type=str,
                description="City station",
                required=False,
            )])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "create":
            return StationCreateSerializer
        return StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        queryset = Route.objects.all().select_related(
            "source__city",
            "destination__city")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteDetailSerializer
        if self.action == "create":
            return RouteCreateSerializer
        return RouteSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer

    def get_queryset(self):
        queryset = Journey.objects.all().select_related(
            "route__source__city",
            "route__destination__city",
            "train"
        ).prefetch_related("crew")
        start = self.request.query_params.get("start")
        finish = self.request.query_params.get("finish")
        if start:
            queryset = queryset.filter(
                route__source__city__name__icontains=start
            )
        if finish:
            queryset = queryset.filter(
                route__destination__city__name__icontains=finish
            )
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "start",
                type=str,
                description="Starting city of the journey",
                required=False,
            ),
            OpenApiParameter(
                "finish",
                type=str,
                description="Destination city of the journey",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return JourneySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "tickets__journey__route",
            "tickets__journey__train",
            "tickets__journey__crew",
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

