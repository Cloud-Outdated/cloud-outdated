from django.conf import settings
from django.db import models

from core.models import BaseModelMixin
from services.base import service_choices


class Subscription(BaseModelMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.CharField(choices=service_choices, max_length=255)
    disabled = models.DateTimeField(
        null=True, blank=True, help_text="If populated date of unsubscribing"
    )
