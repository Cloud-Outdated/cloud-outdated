from core.views import IndexView
from django.contrib import admin
from django.urls import include, path
from users.views import (
    UserSubscriptionsThankYouAboutView,
    UserSubscriptionsView,
    UserLoginView,
    UserLoginThankYouView,
)

urlpatterns = [
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
]
