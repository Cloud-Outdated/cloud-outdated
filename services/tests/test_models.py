from unittest.mock import patch
from grpc import services
from services.tests.factories import VersionFactory
from django.test import TestCase
from services.base import Service, services, aws


class VersionServiceLabelTestCase(TestCase):
    def test_known_service(self):
        version = VersionFactory(deprecated=None)

        assert version.service_label == services[version.service].label

    def test_unknown_service(self):
        version = VersionFactory(deprecated=None, service="foo_bar")

        assert version.service_label == "foo_bar"


class VersionServiceIsPublicTestCase(TestCase):
    def test_service_is_public(self):
        version = VersionFactory(service=services["aws_aurora"].name)

        assert version.service_is_public is True

    def test_service_is_not_public(self):
        non_public_aws_aurora = Service(
            platform=aws,
            name="aws_aurora",
            name_alternatives=[],
            public=False,
        )

        with patch.dict(services, {"aws_aurora": non_public_aws_aurora}):
            version = VersionFactory(service=services["aws_aurora"].name)

            assert version.service_is_public is False

    def test_service_was_not_found(self):
        version = VersionFactory(service="foo_bar")

        assert version.service_is_public is False
