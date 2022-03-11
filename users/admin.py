from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from subscriptions.models import Subscription

from .models import UserProfile


class UserSubscriptionsInline(admin.TabularInline):
    model = Subscription
    readonly_fields = [
        "created",
        "service",
        "disabled",
    ]
    show_change_link = True
    can_delete = False
    extra = 0
    ordering = ["-created"]


@admin.register(UserProfile)
class UserProfileAdmin(DjangoUserAdmin):
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    list_display = [
        "id",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
    ]
    search_fields = ["id", "email", "first_name", "last_name"]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
        "created",
    ]
    ordering = ["created"]
    date_hierarchy = "created"
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    inlines = [UserSubscriptionsInline]
