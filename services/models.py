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
