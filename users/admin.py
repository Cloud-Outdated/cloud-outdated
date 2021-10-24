from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
    ]
    search_fields = ["id", "email"]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
        "created",
    ]
    date_hierarchy = "created"
