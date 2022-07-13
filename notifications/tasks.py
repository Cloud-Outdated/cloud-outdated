import logging

import backoff
import structlog
from django.conf import settings
from django.contrib.auth import get_user_model
from services.models import Version
from subscriptions.models import Subscription

from notifications.models import Notification, NotificationItem

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
        deprecated_version_ids = get_deprecated_versions_for_user(
            user, subscribed_service_keys
        )

        notify_user(user, new_version_ids + deprecated_version_ids)


def get_new_versions_for_user(user, service_keys):
    """Get versions about which user was not notified yet.

    Args:
        user (users.models.UserProfile): user instance
        service_keys (list[str]): list of service keys as stored in db

    Returns:
        list: ids of new versions
    """
    available_version_ids = Version.available(service_keys).values_list("id", flat=True)

    past_notification_version_ids = (
        NotificationItem.objects.filter(
            notification__user=user,
            version__in=available_version_ids,
        )
        .exclude(notification__sent=None)
        .select_related("notification")
        .values_list("version", flat=True)
    )

    new_version_ids = set(available_version_ids) - set(past_notification_version_ids)

    return [str(id) for id in list(new_version_ids)]


def get_deprecated_versions_for_user(user, service_keys):
    """Get deprecated versions about which user was not notified yet.

    Args:
        user (users.models.UserProfile): user instance
        service_keys (list[str]): list of service keys as stored in db

    Returns:
        list: ids of newly deprecated versions
    """
    deprecated_version_ids = Version.unsupported(service_keys).values_list(
        "id", flat=True
    )

    newly_deprecated_version_ids = []

    for version_id in deprecated_version_ids:
        if (
            NotificationItem.objects.filter(
                notification__user=user,
                version=version_id,
            ).count()
            <= 1
        ):
            newly_deprecated_version_ids.append(str(version_id))

    return newly_deprecated_version_ids


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
    versions = Version.objects.filter(id__in=version_ids)

    if len(versions) > 0:
        notification = Notification.objects.create(user=user, sent=None)
        for version in versions:
            NotificationItem.objects.create(notification=notification, version=version)

        # call method that grabs all notification items, sends email and sets sent timestamp
        notification.send()
