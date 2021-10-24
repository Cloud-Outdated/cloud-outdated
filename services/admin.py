from django.contrib import admin

from services.models import Version


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ["id", "service", "version"]
    search_fields = ["id", "service", "version"]
    list_filter = ["service", "created"]
    date_hierarchy = "created"
