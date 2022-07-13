from django.contrib import sitemaps
from django.urls import reverse


class LoginViewSitemap(sitemaps.Sitemap):
    priority = 0.4
    changefreq = "never"

    def items(self):
        return ["user_login"]

    def location(self, item):
        return reverse(item)


class ContentPagesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ["home", "user_subscriptions", "service_list"]

    def location(self, item):
        return reverse(item)
