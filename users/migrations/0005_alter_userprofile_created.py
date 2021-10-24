# Generated by Django 3.2.8 on 2021-10-24 21:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_userprofile_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="created",
            field=models.DateTimeField(
                db_index=True, default=django.utils.timezone.now
            ),
        ),
    ]
