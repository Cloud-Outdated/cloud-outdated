from django.contrib import admin

from notifications.models import Notification, NotificationItem


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "sent", "sent_at"]
    search_fields = ["id", "user__id", "user__email"]
    list_filter = ["sent", "created"]
    list_select_related = ["user"]
    date_hierarchy = "created"


@admin.register(NotificationItem)
class NotificationItemAdmin(admin.ModelAdmin):
    list_display = ["id", "notification", "version"]
    search_fields = ["id", "notification__id", "version__id"]
    list_filter = ["created"]
    list_select_related = ["notification", "version"]
    date_hierarchy = "created"
