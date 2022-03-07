from django.urls import reverse_lazy, reverse
from core.views import BaseView
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from services.base import services
from sesame.utils import get_query_string
from subscriptions.models import Subscription

from .email import UserLoginEmail, UserRegistrationEmail
from .forms import UserSubscriptionsCaptchaForm

User = get_user_model()


class UserSubscriptionsView(FormView, BaseView):
    template_name = "user-subscriptions.html"
    form_class = UserSubscriptionsCaptchaForm
    # TODO redirect to some "Thank you for subscribing! Check you email!" page
    success_url = reverse_lazy("user_subscriptions")
    http_method_names = ["get", "post"]

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

    def subscribe_user(self, user, form):
        for field_name, field_value in form.cleaned_data.items():
            if field_name in services:
                if field_value is True:
                    Subscription.subscribe_user_to_service(user, field_name)
        # TODO unsubscribe user (if logged in and deselects a service)
        # I have a list in active_subscription_services of currently subscribed
        # services, need to get the diff

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        # TODO add validation if user is logged in but email is different

        user = User.objects.filter(email=email).first()
        protocol = "https" if self.request.is_secure() else "http"

        if not user:
            user = User.objects.create(email=email)
            user.set_unusable_password()

            email_ctx = {
                "link": f"{protocol}://"
                + self.request.get_host()
                + reverse("user_subscriptions")
                + get_query_string(user),
            }

            UserRegistrationEmail(context=email_ctx).send(to=[user.email])
        else:
            email_ctx = {
                "link": f"{protocol}://"
                + self.request.get_host()
                + reverse("user_subscriptions")
                + get_query_string(user),
            }
            UserLoginEmail(context=email_ctx).send(to=[user.email])

        self.subscribe_user(user, form)

        return super().form_valid(form)
