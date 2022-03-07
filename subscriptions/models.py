from django.conf import settings
from django.db import models

from core.models import BaseModelMixin
from services.base import services, service_choices


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
        """
        assert service in services

        subscription, _ = cls.objects.get_or_create(
            user=user,
            service=service,
            disabled=None,
        )
        return subscription
