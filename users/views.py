from django.forms import ValidationError
from core.views import BaseView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from services.base import services
from sesame.utils import get_query_string
from subscriptions.models import Subscription

from .email import UserUpdateSubscriptionsEmail, UserRegistrationEmail, UserLoginEmail
from .forms import UserSubscriptionsCaptchaForm, UserLoginForm

User = get_user_model()


class UserSubscriptionsView(FormView, BaseView):
    template_name = "user-subscriptions.html"
    form_class = UserSubscriptionsCaptchaForm
    http_method_names = ["get", "post"]
    success_url = reverse_lazy("user_subscriptions_thank_you")

    def get_active_subscription_services(self):
        """Return list of services the user is currently subscribed to.

        Returns:
            list: keys of services
        """
        if self.request.user.is_authenticated:
            user = self.request.user
            return Subscription.objects.filter(user=user, disabled=None).values_list(
                "service", flat=True
            )
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context[
            "active_subscription_services"
        ] = self.get_active_subscription_services()

        return context

    def subscribe_and_unsubscribe_user(self, user, form, active_subscription_services):
        for field_name, field_value in form.cleaned_data.items():
            if field_name in services:
                if field_value is True:
                    Subscription.subscribe_user_to_service(user, field_name)
                if field_value is False and field_name in active_subscription_services:
                    Subscription.unsubscribe_user_from_service(user, field_name)

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        user = User.objects.filter(email=email).first()

        if not user:
            user = User.objects.create(email=email)
            user.set_unusable_password()

            email_ctx = {
                "link": settings.BASE_URL
                + reverse("user_subscriptions")
                + get_query_string(user),
            }

            UserRegistrationEmail(context=email_ctx).send(to=[user.email])
        else:
            email_ctx = {
                "link": settings.BASE_URL
                + reverse("user_subscriptions")
                + get_query_string(user),
            }
            UserUpdateSubscriptionsEmail(context=email_ctx).send(to=[user.email])

        self.subscribe_and_unsubscribe_user(
            user, form, self.get_context_data()["active_subscription_services"]
        )

        return super().form_valid(form)

    def get_initial(self):
        data = super().get_initial()

        if self.request.user.is_authenticated:
            data["user"] = self.request.user
        else:
            data["user"] = None

        return data


class UserSubscriptionsThankYouAboutView(BaseView):
    template_name = "user-subscriptions-thank-you.html"


class UserLoginView(FormView, BaseView):
    template_name = "user-login.html"
    form_class = UserLoginForm
    http_method_names = ["get", "post"]
    success_url = reverse_lazy("user_login_thank_you")

    # TODO if user is authenticated redirect to user_subscriptions

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        user = User.objects.filter(email=email).first()

        email_ctx = {
            "link": settings.BASE_URL
            + reverse("user_subscriptions")
            + get_query_string(user),
        }
        UserLoginEmail(context=email_ctx).send(to=[user.email])

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """If user is logged in, just redirect him to subscriptions."""
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("user_subscriptions"))
        return super().get(request, *args, **kwargs)


class UserLoginThankYouView(BaseView):
    template_name = "user-login-thank-you.html"

    def get(self, request, *args, **kwargs):
        """If user is logged in, just redirect him to subscriptions."""
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("user_subscriptions"))
        return super().get(request, *args, **kwargs)
