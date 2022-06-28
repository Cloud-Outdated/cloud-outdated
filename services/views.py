from core.views import BaseView
from django.http import Http404

from services.models import Version

from .base import services


class ServiceDetailView(BaseView):
    template_name = "service-detail.html"

    def get(self, request, platform, service_name):
        service_key = f"{platform}_{service_name}"
        if service_key in services:
            return super().get(
                request,
                service=services[service_key],
                available_versions=list(Version.available([service_key])),
                unsupported_versions=list(Version.unsupported([service_key])),
                started_polling=Version.bigbang(service_key),
            )
        raise Http404
