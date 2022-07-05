from django.contrib import sitemaps
from django.urls import reverse

from services.base import services
from services.models import Version


class ServiceDetailViewSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return [s for s in services.values() if s.public]

    def location(self, item):
        return reverse(
            "service_detail",
            args=[item.platform.name, "_".join(item.name.split("_")[1:])],
        )

    def lastmod(self, item):
        last_version = (
            Version.objects.filter(service=item.name).order_by("-created").first()
        )
        if last_version:
            return last_version.created
        return None
