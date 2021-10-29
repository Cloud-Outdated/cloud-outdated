from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils import timezone

from core.models import BaseModelMixin


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a new superuser profile"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractUser, BaseModelMixin):
    """Database model for users in the system"""

    username = None
    email = models.EmailField(max_length=255, unique=True)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Return string representation of our user"""
        return self.email
