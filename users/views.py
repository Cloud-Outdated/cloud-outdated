from core.views import BaseView
from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from django.shortcuts import render
from services.base import aws, azure, gcp, services
from sesame.utils import get_query_string
from subscriptions.models import Subscription

from .email import UserLoginEmail, UserRegistrationEmail
from .forms import UserSubscriptionsCaptchaForm

User = get_user_model()


class UserSubscriptionsView(BaseView):
    template_name = "user-subscriptions.html"

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

        context["aws_services"] = [
            (key, service)
            for key, service in services.items()
            if service.platform == aws and service.public is True
        ]
        context["gcp_services"] = [
            (key, service)
            for key, service in services.items()
            if service.platform == gcp and service.public is True
        ]
        context["azure_services"] = [
            (key, service)
            for key, service in services.items()
            if service.platform == azure and service.public is True
        ]
        context["captcha"] = UserSubscriptionsCaptchaForm()
        return context

    def post(self, request, *args, **kwargs):

        context_data = self.get_context_data(**kwargs)

        context_data[
            "active_subscription_services"
        ] = self.get_active_subscription_services()
        if request.user.is_authenticated:
            return render(request, self.template_name, context_data)

        post_data = request.POST
        email = post_data.get("email")
        protocol = "https" if request.is_secure() else "http"

        if not UserSubscriptionsCaptchaForm(post_data).is_valid():
            raise BadRequest

        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.create(email=email)
            user.set_unusable_password()

            ctx = {
                "link": f"{protocol}://"
                + request.get_host()
                + request.path
                + get_query_string(user),
            }

            UserRegistrationEmail(context=ctx).send(to=[user.email])
        else:
            ctx = {
                "link": f"{protocol}://"
                + request.get_host()
                + request.path
                + get_query_string(user),
            }
            UserLoginEmail(context=ctx).send(to=[user.email])

        return render(request, self.template_name, context_data)
