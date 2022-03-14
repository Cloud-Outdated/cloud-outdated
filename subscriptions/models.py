import structlog
from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import BaseModelMixin
from notifications.models import Notification
from services.base import services, service_choices

logger = structlog.get_logger(__name__)


class Subscription(BaseModelMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.CharField(choices=service_choices, max_length=255)
    disabled = models.DateTimeField(
        null=True, blank=True, help_text="If populated date of unsubscribing"
    )

    @classmethod
    def subscribe_user_to_service(cls, user, service):
        """Subscribe user to service if such service exists and user is not
        already subcribed.

        If user has an active subscription, do not fail, just return that
        subscription instance

        Args:
            user (users.models.UserProfile): user instance
            service (str): service key

        Returns:
            subscriptions.models.Subscription
        """
        assert service in services

        subscription, created = cls.objects.get_or_create(
            user=user,
            service=service,
            disabled=None,
        )

        if created:
            Notification.save_initial_service_subscription(user, service)

        return subscription

    @classmethod
    def unsubscribe_user_from_service(cls, user, service):
        """Unsubscribe user to service if such service exists and user is subcribed.

        If user has an active subscription, mark it as disabled.

        Args:
            user (users.models.UserProfile): user instance
            service (str): service key

        Returns:
            subscriptions.models.Subscription
        """
        assert service in services

        try:
            subscription = cls.objects.get(user=user, service=service, disabled=None)
            subscription.disabled = timezone.now()
            subscription.save()
            return subscription
        except cls.DoesNotExist:
            logger.warning(
                "Unsubscribing from service failed, active subscription not found",
                user_id=user.id,
                service=service,
            )
            return None
