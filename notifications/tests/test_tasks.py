from unittest.mock import call, patch
from notifications.tasks import (
    send_notifications,
    send_user_notification,
    get_new_versions_for_user,
)
from django.test import TestCase
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
