from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

cep_validator = RegexValidator(
    regex=r'^\d{5}-\d{3}$',
    message=_('Enter a valid ZIP code in the format XXXXX-XXX.'),
    code='invalid_cep',
)
