from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

username_validator = RegexValidator(
    regex=r'^[a-z0-9._]+$',
    message=_(
        'This field should contain only lowercase letters, numbers, ".", and "_".'
    ),
    flags=0,
)
