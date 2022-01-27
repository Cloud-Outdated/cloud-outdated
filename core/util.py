from anymail.message import AnymailMessageMixin
from django.conf import settings
from templated_mail.mail import BaseEmailMessage


class NotifyOperatorEmail(BaseEmailMessage, AnymailMessageMixin):
    template_name = "notify_operator.html"


def notify_operator(message):
    ctx = {"message": message}
    NotifyOperatorEmail(context=ctx).send(to=settings.OPERATORS_EMAIL)
