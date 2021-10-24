from django.db import models
from users.models import UserProfile

from core.models import BaseModelMixin
from services.base import service_choices


class Subscription(BaseModelMixin):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service = models.CharField(choices=service_choices, max_length=255)
    disabled = models.DateTimeField(
        null=True, blank=True, help_text="If populated date of unsubscribing"
    )
