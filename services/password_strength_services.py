from wtforms.validators import ValidationError
import re


def password_strength(form, field):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
    if not re.match(pattern, field.data):
        raise ValidationError(
            "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, and one digit."
        )
