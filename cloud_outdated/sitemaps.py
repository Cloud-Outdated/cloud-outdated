from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "never"

    def items(self):
        return ["home", "user_subscriptions", "user_login", "service_list"]

    def location(self, item):
        return reverse(item)
