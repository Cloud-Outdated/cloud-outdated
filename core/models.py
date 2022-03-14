import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModelMixin(models.Model):
    """Base model for all project-related models."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    created = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ("-created",)

    def __str__(self) -> str:
        return str(self.id)
