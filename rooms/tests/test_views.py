from django.test import TestCase
from django.http import Http404
from rooms.models import Room
from users.models import User
from datetime import datetime


class RoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running RoomViewTest
        Create 23 rooms for RoomViewTest
        """
        user = User.objects.create_user("test_user")

        for i in range(1, 24):
            Room.objects.create(
                name=f"Test Room {i}",
                description="Test Description",
                country="KR",
                city="Seoul",
                price=100,
                address="Test Address",
                guests=4,
                beds=2,
                bedrooms=1,
                baths=1,
                check_in=datetime(2019, 1, 1, 9, 30),
                check_out=datetime(2019, 1, 2, 10, 30),
                instant_book=True,
                host=user,
            )

    def test_view_rooms_home_view_default_page(self):
        """Rooms application HomeView test without pagination param
        Check HomeView HttpResponse content data contain right data
        """
        response = self.client.get("/")
        html = response.content.decode("utf8")
        self.assertEqual(200, response.status_code)

        rooms = Room.objects.all().order_by("created_at")[:10]

        self.assertIn("<title>HOME | Airbnb</title>", html)
        self.assertIn('<a href="?page=2">Next</a>', html)

        for room in rooms:
            self.assertIn(f"<a href='/rooms/{room.id}'>", html)
            self.assertIn(f"<h4>{room} / ${room.price}</h4>", html)

    def test_view_rooms_home_view_next_page(self):
        """Rooms application HomeView view test with pagination param
        Check HomeView HttpResponse content data contain right data
        """
        response = self.client.get("/", {"page": 2})
        html = response.content.decode("utf8")
        self.assertEqual(200, response.status_code)

        rooms = Room.objects.all().order_by("created_at")[10:24]

        self.assertIn("<title>HOME | Airbnb</title>", html)
        self.assertIn('<a href="?page=1">Previous</a>', html)

        for room in rooms:
            self.assertIn(f"<a href='/rooms/{room.id}'>", html)
            self.assertIn(f"<h4>{room} / ${room.price}</h4>", html)

    def test_view_rooms_home_view_invalid_page(self):
        """Rooms application HomeView test page param is invalid page
        Check HomeView HttpResponse is redirect to '/' url
        """
        response = self.client.get("/", {"page": "3"})
        self.assertRedirects(response, "/")

    def test_view_rooms_home_view_str_page_param(self):
        """Rooms application HomeView test page param is invalid string
        Check HomeView HttpResponse is redirect to '/' url
        """
        response = self.client.get("/", {"page": "invalid_param"})
        self.assertRedirects(response, "/")

    def test_view_rooms_app_room_detail_success(self):
        """Rooms application room_detail test is success
        Check room_deatil HttpResponse contain right room instance data
        """
        response = self.client.get("/rooms/1")
        html = response.content.decode("utf8")

        self.assertIn("<title>ROOM DETAIL | Airbnb</title>", html)
        self.assertIn(f"<h5>name / Test Room 1</h5>", html)
        self.assertIn(f"<h5>description / Test Description</h5>", html)

    def test_view_rooms_app_room_detail_fail(self):
        """Rooms application room_detail test is fail
        Check room_deatil HttpResponse return status code 404
        """
        response = self.client.get("/rooms/25")
        self.assertEqual(404, response.status_code)
