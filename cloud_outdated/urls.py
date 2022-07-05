from core.views import IndexView, NotFoundView
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from notifications.views import NotificationPixelView
from services.sitemaps import ServiceDetailViewSitemap
from services.views import ServiceDetailView, ServiceListView
from users.views import (
    UserLoginThankYouView,
    UserLoginView,
    UserSubscriptionsThankYouAboutView,
    UserSubscriptionsView,
)

from .sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceDetailViewSitemap,
}

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", IndexView.as_view(), name="home"),
    path(
        "user-subscriptions-thank-you/",
        UserSubscriptionsThankYouAboutView.as_view(),
        name="user_subscriptions_thank_you",
    ),
    path(
        "user-subscriptions/",
        UserSubscriptionsView.as_view(),
        name="user_subscriptions",
    ),
    path(
        "login-thank-you/",
        UserLoginThankYouView.as_view(),
        name="user_login_thank_you",
    ),
    path(
        "login/",
        UserLoginView.as_view(),
        name="user_login",
    ),
    path("dlxusdprq-uzbdhomvw/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "notification-pixel/<str:notification_id>.gif",
        NotificationPixelView.as_view(),
        name="notification_pixel",
    ),
    path(
        "service/<str:platform>/<str:service_name>",
        ServiceDetailView.as_view(),
        name="service_detail",
    ),
    path(
        "services/",
        ServiceListView.as_view(),
        name="service_list",
    ),
]


handler404 = NotFoundView.as_view()
