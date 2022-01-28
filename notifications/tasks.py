from datetime import datetime

import structlog
from django.contrib.auth import get_user_model

from subscriptions.models import Subscription
from services.models import Version
from .models import Notification, NotificationItem

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
    subscribed_service_ids = Subscription.objects.filter(
        user=user, disabled=False
    ).values_list("service", flat=True)

    subscribed_services_count = len(subscribed_service_ids)
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

        new_version_ids = get_new_versions_for_user(user, subscribed_service_ids)

        notify_user(user, new_version_ids)


def get_new_versions_for_user(user, service_ids):
    """Get versions about which user was not notified yet.

    Args:
        user (users.models.UserProfile): user instance
        service_ids (list[str]): list of service names

    Returns:
        list: ids of new versions
    """
    available_version_ids = Version.objects.filter(
        service__in=service_ids,
        deprecated=False,
        released__lte=datetime.today(),
    ).values_list("id", flat=True)

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

    return new_version_ids


def notify_user(user, version_ids):
    """Takes care of creating the Notification object and sending the email.

    Args:
        user (users.models.UserProfile): user instance
        version_ids (list[uuid.UUID]): list of service versions the user will be notified of
    """
    notification = Notification.objects.create(user=user, sent=False)
    for version_id in version_ids:
        NotificationItem.objects.create(notification=notification, version=version_id)
    notification.send()  # call method that grabs all items, sends email and flips sent to True
