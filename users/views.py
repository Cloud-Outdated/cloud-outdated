from django.shortcuts import render

from core.views import BaseView
from services.base import services, aws, gcp, azure

from .email import UserRegistrationEmail


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
        post_data = request.POST

        UserRegistrationEmail().send(to=[post_data.get("email")])
        # return HttpResponseRedirect("/thanks/")

        return render(request, self.template_name, {})
