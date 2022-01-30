from django.conf import settings
from django.db import models
from core.models import BaseModelMixin
from services.models import Version


class Notification(BaseModelMixin):
    """Single notification sent out to the user.

    One or multiple NotificationItem instances are connected with it."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_notifications",
        on_delete=models.CASCADE,
    )
    sent = models.BooleanField(default=False, help_text="switched to True once sent")

    def send(self):
        """Placeholder method that will use NotificationEmail
        to send and email with new service versions.
        """


class NotificationItem(BaseModelMixin):
    """Single service/version about the user will receive notification."""

    notification = models.ForeignKey(
        Notification,
        related_name="notification_items",
        on_delete=models.CASCADE,
    )
    version = models.ForeignKey(
        Version,
        related_name="version_notification_items",
        on_delete=models.CASCADE,
    )
