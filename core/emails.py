from urllib.parse import urlparse

from anymail.message import AnymailMessageMixin
from templated_mail.mail import BaseEmailMessage

from django.conf import settings


class BaseEmail(BaseEmailMessage, AnymailMessageMixin):
    subject_prefix = "Cloud-Outdated.com"
    subject_suffix = ""

    def get_context_data(self, **kwargs):
        """Set email context's defaults."""
        context = super().get_context_data(**kwargs)

        context["subject_prefix"] = self.subject_prefix
        context["subject_suffix"] = self.subject_suffix

        return context
