import factory
from notifications.models import Notification, NotificationItem
from users.tests.factories import UserProfileFactory
from services.tests.factories import VersionFactory


class NotificationFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserProfileFactory)
    sent = True

    class Meta:
        model = Notification


class NotificationItemFactory(factory.django.DjangoModelFactory):
    notification = factory.SubFactory(NotificationFactory)
    version = factory.SubFactory(VersionFactory)

    class Meta:
        model = NotificationItem
