from django.db import models
from django.utils import timezone


class BaseModelMixin(models.Model):
    """Base model for all project-related models."""

    created = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    class Meta:
        abstract = True
