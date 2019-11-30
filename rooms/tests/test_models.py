from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime
from rooms.models import Room, RoomType, Amenity, Facility, HouseRule
from users.models import User
from unittest import mock
import pytz


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running RoomModelTest

        Fields :
            id           : 1
            name         : Test Room 1
            description  : Test Description 1
            country      : KR -> 대한민국
            city         : Seoul
            price        : 100
            address      : Test Address
            guest        : 4
            beds         : 2
            bedrooms     : 1
            baths        : 1
            check_in     : 09-30
            check_out    : 10-30
            instant_book : True
            host         : test_user
            created_at   : 2019.11.30.00.00.00
            updated_at    : 2019.12.01.00.00.00
        """
        user = User.objects.create_user("test_user")
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Room.objects.create(
                name="Test Room 1",
                description="Test Description 1",
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

    def test_room_create_success(self):
        """Room model creation success test
        Check unique field and instance's class name
        """
        room = Room.objects.get(id=1)
        self.assertEqual("Room", room.__class__.__name__)
        self.assertEqual("Test Room 1", room.name)
        self.assertEqual("test_user", room.host.username)

    def test_room_create_fail(self):
        """Room model creation failure test
        Duplicate pk index with IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            Room.objects.create(pk=1, name="Test Room 2")

    def test_room_get_fields(self):
        """Room model get fields data test
        Check room's all fields except when testing create success test
        """
        room = Room.objects.get(id=1)
        self.assertEqual("Test Description 1", room.description)
        self.assertEqual("대한민국", room.country.name)
        self.assertEqual("Seoul", room.city)
        self.assertEqual(100, room.price)
        self.assertEqual("Test Address", room.address)
        self.assertEqual(4, room.guests)
        self.assertEqual(2, room.beds)
        self.assertEqual(1, room.bedrooms)
        self.assertEqual(1, room.baths)
        self.assertEqual(datetime(2019, 1, 1, 9, 30).time(), room.check_in)
        self.assertEqual(datetime(2019, 1, 1, 10, 30).time(), room.check_out)
        self.assertTrue(room.instant_book)

    def test_room_str_method(self):
        """Room model str method test
        Check str method equal room instance name field
        """
        room = Room.objects.get(id=1)
        self.assertEqual(str(room), room.name)

    def test_time_stamp_created_at(self):
        """TimeStamp model created_at test
        Check Test Room 1's created_at field is datetime (2019.11.30)
        """
        room = Room.objects.get(id=1)
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(room.created_at, mocked)

    def test_time_stamp_updated_at(self):
        """TimeStamp model updated_at test
        Get Test Room 1 objects and update Test Room 1 object
        Check Test Room 1's updated_at field is datetime (2019.12.01)
        """
        room = Room.objects.get(id=1)
        mocked = datetime(2019, 12, 1, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            room.beds = 2
            room.save()
            self.assertEqual(room.updated_at, mocked)

    def test_room_room_type_set(self):
        """Room model room_type field test
        Check Room model's room_type equal room_type
        """
        room_type = RoomType(name="Room Type Test")
        room_type.save()

        room = Room.objects.get(id=1)
        room.room_type = room_type
        room.save()

        self.assertEqual(room_type, room.room_type)

    def test_room_amenity_blank(self):
        """Room model amenity field blank test
        Check Room model's amenity field exists equal False
        """
        room = Room.objects.get(id=1)
        self.assertFalse(room.amenities.exists())

    def test_room_one_amenity_set(self):
        """Room model amenity field set one amenity data
        Check Room model's amenity query set equal amenity
        """
        amenity = Amenity.objects.create(name="Test Amenity")
        amenity.save()

        room = Room.objects.get(id=1)
        room.amenities.add(amenity)
        room.save()

        self.assertEqual(amenity, room.amenities.all()[0])

    def test_room_many_amenity_set(self):
        """Room model amenity field set more than one amenities data
        Check Room model's amenity query set equal Amenity model query set
        """
        amenity_1 = Amenity.objects.create(name="Test Amenity 1")
        amenity_1.save()

        amenity_2 = Amenity.objects.create(name="Test Amenity 2")
        amenity_2.save()

        room = Room.objects.get(id=1)
        room.amenities.add(amenity_1)
        room.amenities.add(amenity_2)
        room.save()

        self.assertQuerysetEqual(
            Amenity.objects.all(), map(repr, room.amenities.all()), ordered=False
        )

    def test_room_facilities_blank(self):
        """Room model facilities field blank test
        Check Room model's facilities field exists equal False
        """
        room = Room.objects.get(id=1)
        self.assertFalse(room.facilities.exists())

    def test_room_one_facilities_set(self):
        """Room model facilities field set one facilities data
        Check Room model's facilities query set equal facilities
        """
        facilities = Facility.objects.create(name="Test Facilities")
        facilities.save()

        room = Room.objects.get(id=1)
        room.facilities.add(facilities)
        room.save()

        self.assertEqual(facilities, room.facilities.all()[0])

    def test_room_many_facilities_set(self):
        """Room model facilities field set more than one amenities data
        Check Room model's facilities query set equal facilities model query set
        """
        facilities_1 = Facility.objects.create(name="Test Facilities 1")
        facilities_1.save()

        facilities_2 = Facility.objects.create(name="Test Facilities 2")
        facilities_2.save()

        room = Room.objects.get(id=1)
        room.facilities.add(facilities_1)
        room.facilities.add(facilities_2)
        room.save()

        self.assertQuerysetEqual(
            Facility.objects.all(), map(repr, room.facilities.all()), ordered=False
        )

    def test_room_house_rule_blank(self):
        """Room model house_rules field blank test
        Check Room model's house_rules field exists equal False
        """
        room = Room.objects.get(id=1)
        self.assertFalse(room.house_rules.exists())

    def test_room_one_house_rules_set(self):
        """Room model house_rules field set one house_rules data
        Check Room model's house_rules query set equal house_rules
        """
        house_rule = HouseRule.objects.create(name="Test House Rule")
        house_rule.save()

        room = Room.objects.get(id=1)
        room.house_rules.add(house_rule)
        room.save()

        self.assertEqual(house_rule, room.house_rules.all()[0])

    def test_room_many_house_rules_set(self):
        """Room model house_rules field set more than one amenities data
        Check Room model's house_rules query set equal house_rules model query set
        """
        house_rule_1 = HouseRule.objects.create(name="Test House Rule 1")
        house_rule_1.save()

        house_rule_2 = HouseRule.objects.create(name="Test House Rule 2")
        house_rule_2.save()

        room = Room.objects.get(id=1)
        room.house_rules.add(house_rule_1)
        room.house_rules.add(house_rule_2)
        room.save()

        self.assertQuerysetEqual(
            HouseRule.objects.all(), map(repr, room.house_rules.all()), ordered=False
        )


class RoomTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running RoomTypeModelTest

        Fields :
            id           : 1
            name         : Single room
        """
        RoomType.objects.create(name="Single room")

    def test_room_type_create_success(self):
        """RoomType model create success test
        Check class name and room_type name field
        """
        room_type = RoomType.objects.get(id=1)
        self.assertEqual(room_type.name, "Single room")
        self.assertEqual(room_type.__class__.__name__, "RoomType")

    def test_room_type_str_method(self):
        """RoomType model str method test
        Check str method equal room_type instance name field
        """
        room_type = RoomType.objects.get(id=1)
        self.assertEqual(str(room_type), room_type.name)


class AmenityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running AmenityModelTest

        Fields :
            id           : 1
            name         : Single room
        """
        Amenity.objects.create(name="Single room")

    def test_amenity_create_success(self):
        """Amenity model create success test
        Check class name and amenity name field
        """
        amenity = Amenity.objects.get(id=1)
        self.assertEqual(amenity.name, "Single room")
        self.assertEqual(amenity.__class__.__name__, "Amenity")

    def test_amenity_str_method(self):
        """Amenity model str method test
        Check str method equal amenity instance name field
        """
        amenity = Amenity.objects.get(id=1)
        self.assertEqual(str(amenity), amenity.name)


class FacilityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running FacilityModelTest

        Fields :
            id           : 1
            name         : Single room
        """
        Facility.objects.create(name="Single room")

    def test_facility_create_success(self):
        """Facility model create success test
        Check class name and facility name field
        """
        facility = Facility.objects.get(id=1)
        self.assertEqual(facility.name, "Single room")
        self.assertEqual(facility.__class__.__name__, "Facility")

    def test_facility_str_method(self):
        """Facility model str method test
        Check str method equal facility instance name field
        """
        facility = Facility.objects.get(id=1)
        self.assertEqual(str(facility), facility.name)


class HouseRuleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running HouseRuleModelTest

        Fields :
            id           : 1
            name         : Single room
        """
        HouseRule.objects.create(name="Single room")

    def test_house_rule_create_success(self):
        """HouseRule model create success test
        Check class name and house_rule name field
        """
        house_rule = HouseRule.objects.get(id=1)
        self.assertEqual(house_rule.name, "Single room")
        self.assertEqual(house_rule.__class__.__name__, "HouseRule")

    def test_house_rule_str_method(self):
        """HouseRule model str method test
        Check str method equal house_rule instance name field
        """
        house_rule = HouseRule.objects.get(id=1)
        self.assertEqual(str(house_rule), house_rule.name)
