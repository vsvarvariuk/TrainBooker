from django.db import transaction
from rest_framework import serializers
from train_service.models import (TrainType,
                                 Train,
                                 Order,
                                 Crew,
                                 Journey,
                                 Ticket,
                                 Route,
                                 Station,
                                 City)


class TrainTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo", "train_type")


class TrainSerializer(serializers.ModelSerializer):
    train_type = serializers.CharField(source="train_type.name",
                                       read_only=True)

    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo", "train_type")


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class CrewJourneySerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "full_name",)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name",)


class StationSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = Station
        fields = ("id", "name", "longitude", "latitude", "city")


class StationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "longitude", "latitude", "city")


class RouteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.city", read_only=True)
    destination = serializers.CharField(source="destination.city",
                                        read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteDetailSerializer(serializers.ModelSerializer):
    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ("id", "route",
                  "train", "departure_time",
                  "arrival_time", "crew")


class JourneyListSerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()
    train = serializers.CharField(source="train.name")
    crew = serializers.StringRelatedField(many=True)

    class Meta:
        model = Journey
        fields = ("id", "route",
                  "train", "departure_time",
                  "arrival_time", "crew")

    def get_route(self, obj):
        return f"{obj.route.source.city} - {obj.route.destination.city}"


class JourneyDetailSerializer(serializers.ModelSerializer):
    route = RouteSerializer()
    train = TrainSerializer()
    crew = CrewJourneySerializer(many=True)
    available_tickets = serializers.SerializerMethodField()

    class Meta:
        model = Journey
        fields = ("id", "route",
                  "train", "departure_time",
                  "arrival_time", "crew", "available_tickets")

    def get_available_tickets(self, obj):
        tickets = obj.train.cargo_num * obj.train.places_in_cargo
        sold_tickets = Ticket.objects.filter(journey=obj).count()
        available_tickets = tickets - sold_tickets
        return available_tickets


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey")

    def validate(self, attr):
        seat = attr.get("seat")
        cargo = attr.get("cargo")
        journey = attr.get("journey")
        places_in_cargo = journey.train.places_in_cargo
        cargo_num = journey.train.cargo_num

        Ticket.validate_data(
            seat, cargo, cargo_num, places_in_cargo,
            serializers.ValidationError
        )
        return attr


class TicketOrderSerializer(serializers.ModelSerializer):
    journey = JourneyDetailSerializer()

    class Meta:
        model = Ticket
        fields = ("cargo", "seat", "journey")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderDetailSerializer(serializers.ModelSerializer):
    tickets = TicketOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Train
        fields = ("id", "image")
