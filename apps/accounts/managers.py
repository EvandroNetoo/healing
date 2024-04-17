from django.contrib.auth.models import BaseUserManager
from django.apps.registry import apps

from typing import Any


class UserManager(BaseUserManager):
    def _create_user(
        self,
        username: str = None,
        email: str = None,
        password: str = None,
        **extra_fields: Any,
    ) -> None:
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label,
            self.model._meta.object_name,
        )

        email = self.normalize_email(email)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(
        self,
        username: str = None,
        email: str = None,
        password: str = None,
        **extra_fields: Any,
    ):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username: str = None,
        email: str = None,
        password: str = None,
        **extra_fields: Any,
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super User must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super User must have is_superuser=True')

        return self._create_user(username, email, password, **extra_fields)
