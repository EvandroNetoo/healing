from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from .managers import UserManager
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .validators import username_validator
from utils.validators import (
    min_length_4_validator,
    no_whitespaces,
    min_length_6_validator,
)
from django.apps import apps


class User(AbstractBaseUser, PermissionsMixin):
    password_validators = [
        no_whitespaces,
        min_length_6_validator,
    ]

    email = models.EmailField(
        _('email'),
        unique=True,
        validators=[EmailValidator(message='Email inválido.')],
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator, min_length_4_validator],
    )

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('super user status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = f'{self.name} {self.surname}'
        return full_name.strip()