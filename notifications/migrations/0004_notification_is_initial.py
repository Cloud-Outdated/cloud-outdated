# Generated by Django 3.2.12 on 2022-03-11 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0003_notification_sent"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="is_initial",
            field=models.BooleanField(
                default=False,
                help_text="True if this is only bookkeeping for the initial notification that is not really sent",
            ),
        ),
    ]
