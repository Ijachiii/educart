# my_custom_password_validator.py

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_password_complexity(password):
    if len(password) < 8 or not re.search(r'\d', password):
        raise ValidationError("Password must be at least 8 characters long and contain a numeric character.")
