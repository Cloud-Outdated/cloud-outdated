import factory
from services.models import Version
from services.base import service_choices
import random


class VersionFactory(factory.django.DjangoModelFactory):
    service = factory.Faker("random_element", elements=[k for k, v in service_choices])
    version = factory.LazyAttribute(
        lambda o: f"{random.randint(0, 100)}.{random.randint(0, 100)}.{random.randint(0, 100)}"
    )
    released = None
    deprecated = None

    class Meta:
        model = Version
