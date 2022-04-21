from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from grpc import services
from services.base import Service, aws, services
from services.models import Version
from services.tasks import PollService
from services.tests.factories import VersionFactory


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
