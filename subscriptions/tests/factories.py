import factory
from subscriptions.models import Subscription
from users.tests.factories import UserProfileFactory
from services.base import service_choices


class SubscriptionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserProfileFactory)
    service = factory.Faker("random_element", elements=[k for k, v in service_choices])
    disabled = None

    class Meta:
        model = Subscription
