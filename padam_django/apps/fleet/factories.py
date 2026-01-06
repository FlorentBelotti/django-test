import factory
from datetime import timedelta
from django.utils import timezone
from faker import Faker

from . import models


fake = Faker(['fr'])


class DriverFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory('padam_django.apps.users.factories.UserFactory')

    class Meta:
        model = models.Driver


class BusFactory(factory.django.DjangoModelFactory):
    licence_plate = factory.LazyFunction(fake.license_plate)

    class Meta:
        model = models.Bus


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)
    start_time = factory.LazyFunction(lambda: timezone.make_aware(fake.date_time_this_month()))
    end_time = factory.LazyAttribute(lambda obj: obj.start_time + timedelta(hours=fake.random_int(min=2, max=8)))

    class Meta:
        model = models.BusShift


class BusStopFactory(factory.django.DjangoModelFactory):
    bus_shift = factory.SubFactory(BusShiftFactory)
    place = factory.SubFactory('padam_django.apps.geography.factories.PlaceFactory')
    order = factory.Sequence(lambda n: n)
    stop_time = factory.LazyAttribute(
        lambda obj: obj.bus_shift.start_time + timedelta(minutes=fake.random_int(min=10, max=60))
    )

    class Meta:
        model = models.BusStop
