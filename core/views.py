from django.conf import settings
from django.views.generic.base import TemplateView


class PageTitleMixin:
    def get_page_title(self, context):
        return getattr(self, "page_title", settings.COMPANY_NAME)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.get_page_title(context)

        return context


class BaseView(PageTitleMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_name"] = settings.COMPANY_NAME
        context["site_base_url"] = settings.BASE_URL

        return context


class IndexView(BaseView):
    template_name = "index.html"


class NotFoundView(BaseView):
    template_name = "not-found.html"

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404)
