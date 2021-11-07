from anymail.message import AnymailMessageMixin
from templated_mail.mail import BaseEmailMessage


class NotificationEmail(BaseEmailMessage, AnymailMessageMixin):
    template_name = "notification.html"
