from django.test import TestCase
from django.utils import timezone
from services.base import services
from services.models import Version
from services.tasks import PollService
from services.tests.factories import VersionFactory


class VersionServiceUpdate(TestCase):
    def test_activemq_deprecated_versions(self):
        aws_activemq = services["aws_activemq"]
        version_to_deprecate = VersionFactory(service=aws_activemq.name)

        def _activemq_pollfn():
            return ["active"]

        ps = PollService(service=aws_activemq, poll_fn=_activemq_pollfn)
        ps.poll()

        assert ps.added_versions == _activemq_pollfn()
        assert ps.deprecated_versions == [version_to_deprecate.version]
        assert (
            Version.objects.filter(service=aws_activemq.name)
            .exclude(deprecated=None)
            .count()
            == 1
        )


class VersionServiceIsDeprecatedThenSupportedAgain(TestCase):
    def test_activemq_renew_and_added_support(self):
        aws_activemq = services["aws_activemq"]
        version_to_renew = VersionFactory(
            service=aws_activemq.name, deprecated=timezone.now()
        )
        version_to_deprecate = VersionFactory(service=aws_activemq.name)
        added_version = "5.16.4"

        def poll_supported_versions():
            return [version_to_renew.version, added_version]

        poll_service = PollService(aws_activemq, poll_supported_versions)
        poll_service.poll()

        # Check that the supported versions were added
        assert version_to_renew.version in poll_service.added_versions
        assert added_version in poll_service.added_versions
        assert (
            Version.objects.filter(
                service=aws_activemq.name,
                version__in=poll_supported_versions(),
                deprecated=None,
            ).count()
            == 2
        )

        # Check that the deprecated versions were updated
        assert version_to_deprecate.version in poll_service.deprecated_versions
        assert not Version.objects.filter(
            service=aws_activemq.name,
            version=version_to_deprecate.version,
            deprecated=None,
        ).exists()
