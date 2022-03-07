from grpc import services
from services.tests.factories import VersionFactory
from django.test import TestCase
from services.base import services


class VersionServiceLabelTestCase(TestCase):
    def test_known_service(self):
        version = VersionFactory(deprecated=None)

        assert version.service_label == services[version.service].label

    def test_unknown_service(self):
        version = VersionFactory(deprecated=None, service="foo_bar")

        assert version.service_label == "foo_bar"
