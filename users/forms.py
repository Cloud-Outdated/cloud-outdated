from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django.contrib.auth import get_user_model
from django import forms

from services.base import services

User = get_user_model()


class UserSubscriptionsCaptchaForm(forms.Form):
    email = forms.EmailField(required=True, help_text="Email for notifications")
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #  dynamicaly set all public services as form fields
        for service_key, service_details in services.items():
            if service_details.public is True:
                self.fields[service_key] = forms.BooleanField(
                    required=False,
                    label=service_details.label,
                )
                self.fields[service_key].is_service = True
                self.fields[service_key].platform = service_details.platform


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True, help_text="Email for notifications")
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def clean_email(self):
        data = self.cleaned_data["email"]

        if User.objects.filter(email=data).exists() is False:
            raise forms.ValidationError(
                "There is no account associated with this email address"
            )

        return data
