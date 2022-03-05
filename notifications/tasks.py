import logging
from datetime import datetime

import backoff
import structlog
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from django.conf import settings

from notifications.models import Notification, NotificationItem
from subscriptions.models import Subscription
from services.models import Version

UserProfile = get_user_model()
logger = structlog.get_logger(__name__)

# daily (or n times per day) task that:
# get all Subscriptions that are not disabled
# get all Versions that are not deprecated and released is <= than today


def send_notifications():
    """Send notifications about new versions to subscribed users.

    Main task that will be run periodically which triggers other smaller
    per-user tasks.

    A user should get a grouped notification with all the new versions
    for the services they are subscribed to.
    """
    for user in UserProfile.objects.filter(is_active=True):
        send_user_notification(user)


def send_user_notification(user):
    """Send user notification for new versions.

    Args:
        user (users.models.UserProfile): user instance
    """
    subscribed_service_keys = Subscription.objects.filter(
        user=user, disabled=None
    ).values_list("service", flat=True)

    subscribed_services_count = len(subscribed_service_keys)
    if subscribed_services_count == 0:
        logger.info(
            "No active subscriptions found, skipping.",
            user=str(user.id),
            subscribed_services_count=subscribed_services_count,
        )
    else:
        logger.info(
            "Found active subscriptions.",
            user=str(user.id),
            subscribed_services_count=subscribed_services_count,
        )

        new_version_ids = get_new_versions_for_user(user, subscribed_service_keys)

        notify_user(user, new_version_ids)


def get_new_versions_for_user(user, service_keys):
    """Get versions about which user was not notified yet.

    Args:
        user (users.models.UserProfile): user instance
        service_keys (list[str]): list of service keys as stored in db

    Returns:
        list: ids of new versions
    """
    available_version_ids = (
        Version.objects.filter(
            service__in=service_keys,
        )
        .filter(Q(deprecated__gte=timezone.now()) | Q(deprecated=None))
        .filter(Q(released__lte=datetime.today()) | Q(released=None))
        .values_list("id", flat=True)
    )

    past_notification_version_ids = (
        NotificationItem.objects.filter(
            notification__user=user,
            notification__sent=True,
            version__in=available_version_ids,
        )
        .select_related("notification")
        .values_list("version", flat=True)
    )

    new_version_ids = set(available_version_ids) - set(past_notification_version_ids)

    return [str(id) for id in list(new_version_ids)]


@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=settings.NOTIFICATIONS_MAX_RETRIES,
    max_time=settings.NOTIFICATIONS_MAX_TIME,
    backoff_log_level=logging.WARN,
)
def notify_user(user, version_ids):
    """Takes care of creating the Notification object and sending the email.

    Args:
        user (users.models.UserProfile): user instance
        version_ids (list[uuid.UUID]): list of service versions the user will be notified of
    """
    notification = Notification.objects.create(user=user, sent=False)
    for version_id in version_ids:
        NotificationItem.objects.create(notification=notification, version=version_id)

    # call method that grabs all notification items, sends email and flips sent to True
    notification.send()
