from django.db import models

from core.models import BaseModelMixin
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

    @property
    def service_label(self):
        """Get human readable service name.

        Returns:
            str: service name
        """
        try:
            return services[self.service].label
        except KeyError:
            return self.service

    @property
    def service_is_public(self):
        """Check if instance's service is public.

        Returns:
            bool: True if instance's service is public, False if not
        """
        try:
            return services[self.service].public
        except KeyError:
            return False
