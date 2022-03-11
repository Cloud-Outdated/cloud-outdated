from django.contrib import admin

from notifications.models import Notification, NotificationItem


class NotificationInlineAdmin(admin.TabularInline):
    model = NotificationItem
    extra = 0
    show_change_link = True
    can_delete = False
    raw_id_fields = ["version"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "sent", "is_initial"]
    search_fields = ["id", "user__id", "user__email"]
    list_filter = ["sent", "created", "is_initial"]
    list_select_related = ["user"]
    date_hierarchy = "created"
    inlines = [NotificationInlineAdmin]
    raw_id_fields = ["user"]


@admin.register(NotificationItem)
class NotificationItemAdmin(admin.ModelAdmin):
    list_display = ["id", "notification", "version"]
    search_fields = ["id", "notification__id", "version__id"]
    list_filter = ["created"]
    list_select_related = ["notification", "version"]
    date_hierarchy = "created"
    list_select_related = ["notification", "version"]
    raw_id_fields = ["notification", "version"]
