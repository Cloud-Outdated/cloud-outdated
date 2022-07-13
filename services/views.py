from core.views import BaseView
from django.http import Http404

from services.models import Version

from .base import services


class ServiceDetailView(BaseView):
    template_name = "service-detail.html"

    def get(self, request, service_name):
        service_key = service_name.replace("-", "_")
        if service_key in services and services[service_key].public:
            return super().get(
                request,
                service=services[service_key],
                available_versions=list(Version.available([service_key])),
                unsupported_versions=list(Version.unsupported([service_key])),
                started_polling=Version.bigbang(service_key),
            )
        raise Http404


class ServiceListView(BaseView):
    template_name = "service-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = [s for s in services.values() if s.public]

        return context
