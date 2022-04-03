from core.emails import BaseEmail


class UserRegistrationEmail(BaseEmail):
    template_name = "user_registration_email.html"


class UserLoginEmail(BaseEmail):
    template_name = "user_login_email.html"
