from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms


class UserSubscriptionsCaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
