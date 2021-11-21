from django.test import SimpleTestCase

from services.base import Service, services


class ServiceLabelSetTestCase(SimpleTestCase):
    def test_label_was_set(self):
        dummy = Service(
            platform=None,
            name="foo",
            name_alternatives=[],
            label="bar",
        )
        assert dummy.label == "bar"

    def test_label_was_not_set(self):
        dummy = Service(
            platform=None,
            name="foo",
            name_alternatives=[],
            label=None,
        )
        assert dummy.label == "foo"


class ServicesHaveUniqueNameTestCase(SimpleTestCase):
    def test_service_name_is_unique(self):
        assert len(services) == len(
            set([service.name for service in services.values()])
        )
