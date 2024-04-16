from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

no_whitespaces = RegexValidator(
    regex=r'\s',
    message=_('This field must not use whitespaces.'),
    inverse_match=True,
)

only_numbers = RegexValidator(
    regex=r'^[0-9]+$',
    message=_('This field must contain only numbers.'),
    flags=0,
    code='invalid_only_numbers',
)


def min_length_6_validator(value: str) -> bool:
    if len(value) < 6:
        raise ValidationError(_('Use at least 6 characters.'))


def min_length_4_validator(value: str) -> bool:
    if len(value) < 4:
        raise ValidationError(_('Use at least 4 characters.'))


validate_six_digit_number = RegexValidator(
    regex=r'^\d{6}$',
    message=_('The field must have 6 numeric digits.'),
    code='invalid_six_digit_number',
)