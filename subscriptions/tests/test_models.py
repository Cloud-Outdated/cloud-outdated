import pytest
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from subscriptions.models import Subscription
from subscriptions.tests.factories import SubscriptionFactory
from users.tests.factories import UserProfileFactory
from services.base import services


class SubscriptionSubscribeUserToServiceTestCase(TestCase):
    def setUp(self):
        self.user = UserProfileFactory()

    def test_service_not_found(self):
        with pytest.raises(AssertionError):
            Subscription.subscribe_user_to_service(self.user, "dummy_dummy")

    def test_new_subscription(self):
        new_subscription = Subscription.subscribe_user_to_service(
            user=self.user, service=services["aws_aurora"].name
        )

        assert new_subscription.user == self.user
        assert new_subscription.service == services["aws_aurora"].name
        assert new_subscription.disabled is None

    def test_existing_subscription(self):
        existing_subscription = SubscriptionFactory(user=self.user)

        new_subscription = Subscription.subscribe_user_to_service(
            user=self.user, service=existing_subscription.service
        )

        assert new_subscription == existing_subscription
        assert new_subscription.disabled is None


class SubscriptionUnsubscribeUserFromServiceTestCase(TestCase):
    def setUp(self):
        self.user = UserProfileFactory()

    def test_service_not_found(self):
        with pytest.raises(AssertionError):
            Subscription.unsubscribe_user_from_service(self.user, "dummy_dummy")

    def test_no_active_service_subscription(self):
        SubscriptionFactory(
            user=self.user,
            service=services["aws_aurora"].name,
            disabled=timezone.now() - timedelta(days=1),
        )

        subscription = Subscription.unsubscribe_user_from_service(
            self.user, services["aws_aurora"].name
        )

        assert subscription is None

    def test_active_service_subscription(self):
        SubscriptionFactory(
            user=self.user, service=services["aws_aurora"].name, disabled=None
        )

        subscription = Subscription.unsubscribe_user_from_service(
            self.user, services["aws_aurora"].name
        )

        assert subscription.disabled is not None
