from unittest.mock import patch
from django.utils import timezone
from datetime import timedelta
from django.test import TestCase
from notifications.models import Notification
from notifications.tests.factories import NotificationFactory, NotificationItemFactory
from notifications.email import NotificationEmail
from services.tests.factories import VersionFactory
from moto import mock_ses
from django.test.utils import override_settings
from users.tests.factories import UserProfileFactory
from services.base import Service, services, aws


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
        notification.sent is not None

        from django.conf import settings

        assert email.subject == NotificationEmail.subject
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
        notification.sent is not None
        assert email.subject == NotificationEmail.subject
        assert email.to == [self.user.email]
        assert "New versions" not in email.html
        assert "Deprecated versions" in email.html
        assert version.service_label in email.html
        assert version.version in email.html

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
