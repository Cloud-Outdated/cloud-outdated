from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms
from django.contrib.auth import get_user_model
from services.base import services

User = get_user_model()


class UserSubscriptionsCaptchaForm(forms.Form):
    email = forms.EmailField(required=True, help_text="Email for notifications")
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = kwargs["initial"].get("user")

        #  dynamicaly set all public services as form fields
        for service_key, service_details in services.items():
            if service_details.public is True:
                self.fields[service_key] = forms.BooleanField(
                    required=False,
                    label=service_details.label,
                )
                self.fields[service_key].is_service = True
                self.fields[service_key].platform = service_details.platform

    def clean(self):
        super().clean()
        selected_services = []
        for field_name, field_value in self.cleaned_data.items():
            if field_name in services:
                if field_value is True:
                    selected_services.append(field_name)
        if not selected_services and not self.user:
            # Adding the error to the email field just for the purpose of looking good in the UI
            self.add_error(
                "email", "You need to select at least 1 service in order to signup."
            )

    def clean_email(self):
        data = self.cleaned_data["email"]

        if self.user and self.user.email != data:
            raise forms.ValidationError("You cannot update your email.")

        return data


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
