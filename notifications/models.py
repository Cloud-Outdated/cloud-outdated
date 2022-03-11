import structlog

from django.conf import settings
from django.utils import timezone
from django.db import models

from core.models import BaseModelMixin
from notifications.email import NotificationEmail
from services.models import Version


logger = structlog.get_logger(__name__)


class Notification(BaseModelMixin):
    """Single notification sent out to the user.

    One or multiple NotificationItem instances are connected with it."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_notifications",
        on_delete=models.CASCADE,
    )
    sent = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If populated timestamp when the notification was sent, if not, notification was not sent yet",
    )
    is_initial = models.BooleanField(
        default=False,
        help_text="True if this is only bookkeeping for the initial notification that is not really sent",
    )

    def send(self):
        """Send an email to the user and notify that new versions of their
        subscribed services exist.

        This method is ideally used in an async-task.

        Returns:
            notifications.email.NotificationEmail or None: email object if sent, None if not
        """
        logger.bind(notification_id=self.id)

        notification_items = self.notification_items.all()
        new_versions = []
        deprecated_versions = []
        for item in notification_items:
            if item.version.service_is_public is True:
                if item.version.deprecated:
                    deprecated_versions.append(item.version)
                else:
                    new_versions.append(item.version)

        if not new_versions and not deprecated_versions:
            logger.info("Notification sending aborted: nothing to report")
            return None

        ctx = {
            "new_versions": new_versions,
            "deprecated_versions": deprecated_versions,
        }

        email = NotificationEmail(context=ctx)
        email.send(to=[self.user.email])

        if email.anymail_status and hasattr(email.anymail_status, "message_id"):
            self.sent = timezone.now()
            self.save()
            logger.info("Notification sending succeeded")
        else:
            logger.error(
                "Notification sending failed", anymail_status=email.anymail_status
            )
            return None

        logger.unbind("notification_id")
        return email


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
