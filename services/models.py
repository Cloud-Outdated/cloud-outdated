from django.db import models

from core.models import BaseModelMixin
from .base import service_choices


class Version(BaseModelMixin):
    """Service version as reported by the provider."""

    created = models.DateTimeField(...)
    service = models.CharField(choices=service_choices, max_length=255)
    version = models.CharField()
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
