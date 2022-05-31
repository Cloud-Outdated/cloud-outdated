# Generated by Django 3.2.12 on 2022-05-12 21:51

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0004_notification_is_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificationPixel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("metadata", models.JSONField()),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification_pixels",
                        to="notifications.notification",
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
                "abstract": False,
            },
        ),
    ]