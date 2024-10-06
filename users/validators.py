from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def phone_number_validator(value):
    if len(value) != 11:
        raise ValidationError(message=_("The number of digits must be exactly 11!"), code="length")
    if not value.isdigit():
        raise ValidationError(message=_("Only digit is allowed!"), code="digits")
    if  not value.startswith('09'):
        raise ValidationError(message=_("The phone number must start with '09'."), code="prefix")
