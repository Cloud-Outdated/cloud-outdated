from anymail.message import AnymailMessageMixin
from templated_mail.mail import BaseEmailMessage


class UserRegistrationEmail(BaseEmailMessage, AnymailMessageMixin):
    template_name = "user_registration_email.html"
