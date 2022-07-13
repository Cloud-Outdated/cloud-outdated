from django.conf import settings
from django.db import migrations


def setup_default_site(apps, schema_editor):
    """
    Set up or rename the default example.com site created by Django.
    """
    Site = apps.get_model("sites", "Site")

    site_id = settings.SITE_ID
    name = settings.COMPANY_NAME
    domain = settings.BASE_URL.split("//")[1]

    try:
        site = Site.objects.get(domain="example.com")
        site.name = name
        site.domain = domain
        site.save()

    except Site.DoesNotExist:
        # No site with domain example.com exists.
        # Create a default site, but only if no sites exist.
        Site.objects.create(id=site_id, name=name, domain=domain)


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(setup_default_site, migrations.RunPython.noop),
    ]
