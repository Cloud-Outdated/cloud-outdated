from django.contrib import admin

from services.models import Version
from services.base import services


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ["id", "platform", "service", "version"]
    search_fields = ["id", "service", "version"]
    list_filter = ["service", "created"]
    date_hierarchy = "created"

    def platform(self, obj):
        service = services.get(obj.service)
        if service:
            return service.platform.name
        else:
            return "-"
