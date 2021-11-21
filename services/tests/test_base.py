from django.test import SimpleTestCase

from services.base import services


class ServicesHaveUniqueNameTestCase(SimpleTestCase):
    def test_service_name_is_unique(self):
        assert len(services) == len(
            set([service.name for service in services.values()])
        )
