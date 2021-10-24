from django.contrib import admin

from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "service", "disabled"]
    raw_id_fields = ["user"]
    search_fields = ["id", "user__id", "user__email", "service"]
    list_filter = ["service", "created"]
    date_hierarchy = "created"
    list_select_related = ["user"]
