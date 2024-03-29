# Generated by Django 3.2.12 on 2022-03-06 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0002_remove_notification_sent"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="sent",
            field=models.DateTimeField(
                blank=True,
                help_text="If populated timestamp when the notification was sent, if not, notification was not sent yet",
                null=True,
            ),
        ),
    ]
