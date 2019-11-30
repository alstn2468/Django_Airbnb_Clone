from django.db import models
from django_countries.fields import CountryField
from core.models import AbstractTimeStamp
from users.models import User


class AbstractItem(AbstractTimeStamp):
    """Abstract Item Model

    Inherit:
        AbstractTimeStamp

    Fields:
        name : CharField
    """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """RoomType Model
    
    Inherit:
        AbstractItem
    """

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):
    """Amenity Model

    Inherit:
        AbstractItem
    """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility Model

    Inherit:
        AbstractItem
    """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRule Model

    Inherit:
        AbstractItem
    """

    class Meta:
        verbose_name = "House Rule"


class Room(AbstractTimeStamp):
    """Room Model

    Inherit:
        AbstractTimeStamp

    Fields:
        name         : CharField
        description  : TextField
        country      : CountryField
        city         : CharField
        price        : IntegerField
        address      : CharField
        guests       : IntegerField
        beds         : IntegerField
        bedrooms     : IntegerField
        baths        : IntegerField
        check_in     : TimeField
        check_out    : TimeField
        instant_book : BooleanField
        host         : users app User model (1:N)
        room_type    : RoomType model (1:N)
        amenities    : Amenity model (N:N)
        facilities   : Facility model (N:N)
        house_rules  : HouseRule model(N:N)
    """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity)
    facilities = models.ManyToManyField(Facility)
    house_rules = models.ManyToManyField(HouseRule)

    def __str__(self):
        return self.name
