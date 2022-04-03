from core.emails import BaseEmail


class UserRegistrationEmail(BaseEmail):
    template_name = "user_registration_email.html"
    subject_suffix = "Confirm subscription to Cloud Outdated"


class UserLoginEmail(BaseEmail):
    template_name = "user_login_email.html"
    subject_suffix = "Login to Cloud Outdated"
