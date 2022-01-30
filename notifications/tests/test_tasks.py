from unittest.mock import call, patch
from django.utils import timezone
from datetime import timedelta
from notifications.tasks import (
    send_notifications,
    send_user_notification,
    get_new_versions_for_user,
)
from django.test import TestCase
from notifications.tests.factories import NotificationFactory, NotificationItemFactory
from subscriptions.tests.factories import SubscriptionFactory
from services.tests.factories import VersionFactory
from users.tests.factories import UserProfileFactory


class SendNotificationsTestCase(TestCase):
    @patch("notifications.tasks.send_user_notification")
    def test_no_active_users(self, mocked_send_user_notification):
        UserProfileFactory(is_active=False)

        send_notifications()

        mocked_send_user_notification.assert_not_called()

    @patch("notifications.tasks.send_user_notification")
    def test_with_active_users(self, mocked_send_user_notification):
        user_1 = UserProfileFactory(is_active=True)
        user_2 = UserProfileFactory(is_active=True)
        user_3 = UserProfileFactory(is_active=False)

        send_notifications()

        calls = [call(user_1), call(user_2)]
        mocked_send_user_notification.assert_has_calls(calls, any_order=True)


class SendUserNotificationTestCase(TestCase):
    def setUp(self):
        self.user = UserProfileFactory()

    @patch("notifications.tasks.notify_user")
    def test_no_subscriptions(self, mocked_notify_user):
        send_user_notification(self.user)

        mocked_notify_user.assert_not_called()

    @patch("notifications.tasks.notify_user")
    def test_no_enabled_subscriptions(self, mocked_notify_user):
        SubscriptionFactory(user=self.user, disabled=timezone.now() - timedelta(days=1))

        send_user_notification(self.user)

        mocked_notify_user.assert_not_called()

    @patch("notifications.tasks.notify_user")
    def test_enabled_subscriptions(self, mocked_notify_user):
        SubscriptionFactory(user=self.user, disabled=None)

        send_user_notification(self.user)

        mocked_notify_user.assert_called_once()


class GetNewVersionsForUserTestCase(TestCase):
    def test_new_versions(self):
        user = UserProfileFactory()

        version_1 = VersionFactory(deprecated=None)
        version_2 = VersionFactory(deprecated=timezone.now() - timedelta(days=1))
        version_3 = VersionFactory()  # already notified version

        past_notification = NotificationFactory(user=user, sent=True)
        NotificationItemFactory(notification=past_notification, version=version_3)

        service_keys = [version_1.service, version_2.service, version_3.service]

        result = get_new_versions_for_user(user, service_keys)
        assert len(result) == 1
        assert result[0] == str(version_1.id)
