from django.shortcuts import render
from django.contrib.auth import get_user_model
from sesame.utils import get_query_string

from core.views import BaseView
from services.base import services, aws, gcp, azure

from .email import UserLoginEmail, UserRegistrationEmail


User = get_user_model()


class UserSubscriptionsView(BaseView):
    template_name = "user-subscriptions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["aws_services"] = [
            (key, service)
            for key, service in services.items()
            if service.platform == aws
        ]
        context["gcp_services"] = [
            (key, service)
            for key, service in services.items()
            if service.platform == gcp
        ]
        context["azure_services"] = [
            (key, service)
            for key, service in services.items()
            if service.platform == azure
        ]
        return context

    def post(self, request, *args, **kwargs):

        context_data = self.get_context_data(**kwargs)

        if request.user.is_authenticated:
            return render(request, self.template_name, context_data)

        post_data = request.POST
        email = post_data.get("email")
        protocol = "https" if request.is_secure() else "http"

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
