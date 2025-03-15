from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ticket_train.models import (Route, Station,
                                 City, TrainType,
                                 Train, Journey, Crew)


def create_journey():
    train_type = TrainType.objects.create(name="TrainTypeTest")

    train = Train.objects.create(name="TrainTest",
                                 cargo_num=30,
                                 places_in_cargo=4,
                                 train_type=train_type)

    crew = Crew.objects.create(first_name="Jaims",
                               last_name="Williams")

    city_1 = City.objects.create(name="Chernivtsi")
    city_2 = City.objects.create(name="Odessa")

    station_1 = Station.objects.create(name="Test station 1",
                                       latitude=35.345,
                                       longitude=45.456,
                                       city=city_1)

    station_2 = Station.objects.create(name="Test station 2",
                                       latitude=45.345,
                                       longitude=34.567,
                                       city=city_2)

    route = Route.objects.create(source=station_1,
                                 destination=station_2,
                                 distance=450)

    journey = Journey.objects.create(
        route=route,
        train=train,
        departure_time=datetime(2025, 3, 20, 10, 0),
        arrival_time=datetime(2025, 3, 20, 13, 30)
    )
    journey.crew.add(crew)
    return journey


class NonAuthenticateUser(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_no_access_for_not_authenticate_user(self):
        res = self.client.get(reverse("ticket_train:journey-list"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticateUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="testuser@gmail.com",
            password="testuser12345"
        )
        self.client.force_authenticate(user=self.user)

    def test_journey_list_is_allow(self):
        res = self.client.get(reverse("ticket_train:journey-list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_journey_detail_is_allow(self):
        journey = create_journey()
        res = self.client.get(reverse("ticket_train:journey-detail",
                                      args=[journey.id]))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        expected_route = {
            "id": journey.route.id,
            "source": journey.route.source.city.name,
            "destination": journey.route.destination.city.name,
            "distance": journey.route.distance
        }
        self.assertEqual(res.data["route"], expected_route)

    def test_post_not_allow(self):
        journey = create_journey()
        data = {
            "route": journey.route.id,
            "train": journey.train.id,
            "departure_time": journey.departure_time,
            "arrival_time": journey.arrival_time,
            "crew": [crew.id for crew in journey.crew.all()]
        }
        res = self.client.post(reverse("ticket_train:journey-list"), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_not_allow(self):
        journey = create_journey()
        data = {
            "arrival_time": datetime(2025, 4, 30, 11, 25)
        }
        res = self.client.patch(reverse("ticket_train:journey-detail",
                                        args=[journey.id]), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_no_allow(self):
        journey = create_journey()
        data = {
            "arrival_time": datetime(2025, 4, 30, 11, 25)
        }
        res = self.client.put(reverse("ticket_train:journey-detail",
                                      args=[journey.id]), data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_station_by_city(self):
        city_1 = City.objects.create(name="Chernivtsi")
        city_2 = City.objects.create(name="Cherkasy")
        station_1 = Station.objects.create(
            name="stationtest1",
            latitude=45.35,
            longitude=35.34,
            city=city_1
        )
        station_2 = Station.objects.create(
            name="stationtest2",
            latitude=46.35,
            longitude=39.34,
            city=city_2
        )

        res = self.client.get(reverse("ticket_train:station-list"),
                              {"city": "chernivtsi"}
                              )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for station in res.data["results"]:
            self.assertEqual(station["city"], station_1.city.name)
        res_2 = self.client.get(reverse("ticket_train:station-list"),
                                {"city": "cherkasy"}
                                )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for station in res_2.data["results"]:
            self.assertEqual(station["city"], station_2.city.name)

    def test_filter_journey_by_start(self):
        journey = create_journey()
        res = self.client.get(reverse("ticket_train:journey-list"),
                              data={"start": "chernivtsi"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = (f"{journey.route.source.city}"
                    f" - {journey.route.destination.city}")

        for routes in res.data["results"]:
            self.assertEqual(routes["route"], res_data)

        res2 = self.client.get(reverse("ticket_train:journey-list"),
                               data={"start": "Odessa"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        for routes in res2.data["results"]:
            self.assertEqual(routes["route"], [])

    def test_filter_journey_by_finish(self):
        journey = create_journey()
        res = self.client.get(reverse("ticket_train:journey-list"),
                              data={"finish": "chernivtsi"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for routes in res.data["results"]:
            self.assertEqual(routes["route"], [])
        res2 = self.client.get(reverse("ticket_train:journey-list"),
                               data={"finish": "Odessa"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = (f"{journey.route.source.city}"
                    f" - {journey.route.destination.city}")

        for routes in res2.data["results"]:
            self.assertEqual(routes["route"], res_data)


class AdminUserTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="email@gmail.com",
            password="test12345",
            is_staff=True
        )
        self.client.force_authenticate(user=self.user)

    def test_post_is_allow(self):
        data = {
            "name": "Express"
        }
        res = self.client.post(reverse("ticket_train:traintype-list"), data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], "Express")

    def test_put_is_allow(self):
        type_train = TrainType.objects.create(name="Test")
        data = {
            "name": "Express"
        }
        res = self.client.put(reverse(
            "ticket_train:traintype-detail",
            args=[type_train.id]), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], "Express")

    def test_patch_is_allow(self):
        crew = Crew.objects.create(
            first_name="Eric",
            last_name="Garcia"
        )
        data = {
            "first_name": "John"
        }
        res = self.client.patch(reverse(
            "ticket_train:crew-detail",
            args=[crew.id]), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["first_name"], "John")

    def test_admin_can_delete(self):
        type_train_1 = TrainType.objects.create(name="Test_1")
        res = self.client.delete(reverse(
            "ticket_train:traintype-detail",
            args=[type_train_1.id]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
