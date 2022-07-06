from datetime import datetime

from core.models import BaseModelMixin
from django.db import models
from django.db.models import Q
from django.utils import timezone

from .base import service_choices, services


class Version(BaseModelMixin):
    """Service version as reported by the provider."""

    service = models.CharField(choices=service_choices, max_length=255)
    version = models.CharField(max_length=100)
    released = models.DateField(
        null=True,
        blank=True,
        help_text="Only set if known, if missing DOES NOT mean it is not available",
    )  # not all services provide this info clearly
    deprecated = models.DateField(
        null=True, blank=True, help_text="If date of deprecation is known"
    )
    # TODO region availability

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["service", "version"],
                name="unique_service_version",
            ),
        ]

    @classmethod
    def available(cls, service_list):
        """List of available versions for a given service list.

        Args:
            service_list (List): Service names as stored in db

        Returns:
            QuerySet: Available versions ordered by 'version' desc.
        """
        return (
            cls.objects.filter(
                service__in=service_list,
            )
            .filter(Q(deprecated__gte=timezone.now()) | Q(deprecated=None))
            .filter(Q(released__lte=datetime.today()) | Q(released=None))
        ).order_by("-version")

    @classmethod
    def unsupported(cls, service_list):
        """List of unsupported versions for a given service list.

        Args:
            service_list (List): Service names as stored in db

        Returns:
            QuerySet: Unsupported versions ordered by 'version' desc.
        """
        return (
            cls.objects.filter(
                service__in=service_list,
            )
            .filter(Q(deprecated__lt=timezone.now()))
            .order_by("-version")
        )

    @classmethod
    def bigbang(cls, service_name):
        """Returns the beginning of time since we started polling for a particular service.

        Args:
            service_name (str): Service name as stored in db

        Returns:
            Optional[datetime]: Date since we started polling.
        """
        oldest_record = (
            cls.objects.filter(service=service_name).order_by("created").first()
        )
        if oldest_record:
            return oldest_record.created
        return None

    def __str__(self) -> str:
        return f"{str(self.id)} | {self.service} {self.version}"

    @property
    def service_obj(self):
        """Get service object for given version.service choice.

        Returns:
            services.base.Service or None
        """
        try:
            return services[self.service]
        except KeyError:
            return None

    @property
    def service_label(self):
        """Get human readable service name.

        Returns:
            str: service name
        """
        if self.service_obj:
            return self.service_obj.label
        else:
            return self.service

    @property
    def service_is_public(self):
        """Check if instance's service is public.

        Returns:
            bool: True if instance's service is public, False if not
        """
        if self.service_obj:
            return self.service_obj.public
        else:
            return False
