from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.utils import timezone
from moto import mock_ses
from notifications.email import NotificationEmail
from notifications.models import Notification
from notifications.tests.factories import NotificationFactory, NotificationItemFactory
from services.base import Service, aws, services
from services.tests.factories import VersionFactory
from sesame.utils import get_query_string
from users.tests.factories import UserProfileFactory


@override_settings(EMAIL_BACKEND="anymail.backends.test.EmailBackend")
class NotifactionSendTestCase(TestCase):
    def setUp(self) -> None:
        self.user = UserProfileFactory()
        return super().setUp()

    def test_nothing_to_report(self):
        notification = NotificationFactory(
            user=self.user,
        )

        assert notification.send() is None

    @mock_ses
    def test_new_versions(self):
        notification = NotificationFactory(user=self.user, sent=None)
        version = VersionFactory(deprecated=None)
        NotificationItemFactory(notification=notification, version=version)

        email = notification.send()

        notification.refresh_from_db()
        assert notification.sent is not None

        email_template = NotificationEmail(context=email.context)
        email_template.render()
        assert email.subject == email_template.subject
        assert email.to == [self.user.email]
        assert "New versions" in email.html
        assert "Deprecated versions" not in email.html
        assert version.service_label in email.html
        assert version.version in email.html

    def test_deprecated_versions(self):
        notification = NotificationFactory(user=self.user, sent=None)
        version = VersionFactory(deprecated=timezone.now() - timedelta(days=1))
        NotificationItemFactory(notification=notification, version=version)

        email = notification.send()

        notification.refresh_from_db()
        assert notification.sent is not None

        email_template = NotificationEmail(context=email.context)
        email_template.render()
        assert email.subject == email_template.subject
        assert email.to == [self.user.email]
        assert "New versions" not in email.html
        assert "Deprecated versions" in email.html
        assert version.service_label in email.html
        assert version.version in email.html
        assert "Unsubscribe or update your subscriptions" in email.html
        assert settings.BASE_URL + reverse("user_subscriptions") in email.html

    def test_notification_pixel(self):
        notification = NotificationFactory(user=self.user, sent=None)
        version = VersionFactory(deprecated=timezone.now() - timedelta(days=1))
        NotificationItemFactory(notification=notification, version=version)

        email = notification.send()

        assert (
            settings.BASE_URL
            + reverse("notification_pixel", args=[str(notification.id)])
            in email.html
        )

    def test_ordered_versions(self):
        notification = NotificationFactory(user=self.user, sent=None)
        for _ in range(10):
            version_deprecated = VersionFactory(
                deprecated=timezone.now() - timedelta(days=1)
            )
            NotificationItemFactory(
                notification=notification, version=version_deprecated
            )
        for _ in range(10):
            version_released = VersionFactory(
                released=timezone.now() - timedelta(days=1)
            )
            NotificationItemFactory(notification=notification, version=version_released)

        email = notification.send()
        new_versions = email.context["new_versions"]
        deprecated_versions = email.context["deprecated_versions"]

        version_ordering_key = lambda version: (
            version.service_obj.platform.label,
            version.service_label,
            version.version,
        )

        assert new_versions == sorted(new_versions, key=version_ordering_key)
        assert deprecated_versions == sorted(
            deprecated_versions, key=version_ordering_key
        )

        notification.refresh_from_db()
        assert notification.sent is not None

    def test_new_versions_service_not_public(self):
        non_public_aws_aurora = Service(
            platform=aws,
            name="aws_aurora",
            name_alternatives=[],
            public=False,
        )

        with patch.dict(services, {"aws_aurora": non_public_aws_aurora}):
            notification = NotificationFactory(user=self.user, sent=None)
            version = VersionFactory(service=services["aws_aurora"].name)
            NotificationItemFactory(notification=notification, version=version)

            email = notification.send()

            notification.refresh_from_db()
            assert notification.send() is None


class NotificationSaveInitialServiceSubscriptionTestCase(TestCase):
    def setUp(self) -> None:
        self.user = UserProfileFactory()
        return super().setUp()

    def test_multiple_versions(self):
        VersionFactory(service=services["aws_aurora"].name, version="1.0")
        VersionFactory(service=services["aws_aurora"].name, version="2.0")
        VersionFactory(service=services["aws_aurora"].name, version="3.0")

        notification = Notification.save_initial_service_subscription(
            self.user, services["aws_aurora"].name
        )

        assert notification.is_initial is True
        all_versions = notification.notification_items.all().values_list(
            "version__version", flat=True
        )
        assert len(all_versions) == 3
        assert "1.0" in all_versions
        assert "2.0" in all_versions
        assert "3.0" in all_versions
