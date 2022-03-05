from anymail.message import AnymailMessageMixin
from templated_mail.mail import BaseEmailMessage


class NotificationEmail(BaseEmailMessage, AnymailMessageMixin):
    subject = "Cloud-Outdated.com - New service versions updates"
    template_name = "notification.html"
