from django.db import models
from users.models import UserProfile
from django.utils import timezone
from djchoices import ChoiceItem, DjangoChoices


class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    deleted = models.DateTimeField(null=True, default=None)

    class Providers(DjangoChoices):
        AWS = ChoiceItem()
        Gcloud = ChoiceItem()
        Azure = ChoiceItem()

    provider = models.CharField(max_length=20, choices=Providers.choices)

    class AWSServices(DjangoChoices):
        EKS = ChoiceItem()
        # ...

    class GcloudServices(DjangoChoices):
        GKS = ChoiceItem()
        # ...

    class AzureServices(DjangoChoices):
        AKS = ChoiceItem()
        # ...

    service = models.CharField(
        max_length=255,
        choices=(AWSServices.choices + GcloudServices.choices + AzureServices.choices),
    )
