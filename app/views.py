from django.conf import settings
from django.views.generic.base import TemplateView


class PageTitleMixin:
    def get_page_title(self, context):
        return getattr(self, "page_title", f"{settings.COMPANY_NAME} - {settings.DUMMY_VALUE}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.get_page_title(context)

        return context


class BaseView(PageTitleMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_name"] = settings.COMPANY_NAME

        return context


class IndexView(BaseView):
    template_name = "index.html"


class AboutView(BaseView):
    template_name = "about.html"
