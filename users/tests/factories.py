import factory
from users.models import UserProfile


class UserProfileFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    is_active = True

    class Meta:
        model = UserProfile
        django_get_or_create = ("email",)
