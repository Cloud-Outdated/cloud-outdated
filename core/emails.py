from urllib.parse import urlparse

from anymail.message import AnymailMessageMixin
from templated_mail.mail import BaseEmailMessage

from django.conf import settings


class BaseEmail(BaseEmailMessage, AnymailMessageMixin):
    subject_prefix = "Cloud-Outdated.com"

    def get_context_data(self, **kwargs):
        """Set email context's defaults."""
        context = super().get_context_data(**kwargs)

        context["subject_prefix"] = self.subject_prefix

        return context
