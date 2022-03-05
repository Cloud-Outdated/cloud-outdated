import structlog

from django.conf import settings
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
    sent = models.BooleanField(default=False, help_text="switched to True once sent")
    # TODO
    # sent_at = models.DateTimeField()

    def send(self):
        """Send an email to the user and notify that new versions of their
        subscribed services exist.

        This method is ideally used in an async-task.

        Returns:
            notifications.email.NotificationEmail or None: email object if sent, None if not
        """
        logger.bind(notification_id=self.id)

        items = self.notification_items.all()
        new_versions = []
        deprecated_versions = []
        for item in items:
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
            self.sent = True
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
