import pathlib
import uuid

from django.db import models

from django.conf import settings
from django.utils.text import slugify


class TrainType(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    new_file_name = (f"{slugify(instance.name)}-{uuid.uuid4()}"
                     + pathlib.Path(filename).suffix)

    return f"uploads/{new_file_name}"


class Train(models.Model):
    name = models.CharField(max_length=65)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.train_type})"


class Crew(models.Model):
    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class City(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=65)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Route(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE,
                               related_name="sources")

    destination = models.ForeignKey(Station, on_delete=models.CASCADE,
                                    related_name="destinations")
    distance = models.IntegerField()

    def __str__(self):
        return (f"{self.source.name} to "
                f"{self.destination.name} ({self.distance} km)")


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="journeys")

    def __str__(self):
        return (f"Journey on {self.train.name} from "
                f"{self.route.source.name} to "
                f"{self.route.destination.name} at "
                f"{self.departure_time}")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Order by {self.user} at {self.created_at}"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE,
                                related_name="journeys")

    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name="tickets")

    def __str__(self):
        return (f"{self.journey.route.source.city} "
                f"- {self.journey.route.destination.city}, "
                f"departure time {self.journey.departure_time}")

    @staticmethod
    def validate_data(cargo, seat, cargo_num, places_in_cargo, errors):
        if not (1 <= cargo <= cargo_num):
            raise errors(f"Cargo num must be between 1 and {cargo_num}.")

        if not (1 <= seat <= places_in_cargo):
            raise errors(f"Seat number must be "
                         f"between 1 and {places_in_cargo}.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cargo', 'seat'],
                                    name='unique_cargo_seat')
        ]

