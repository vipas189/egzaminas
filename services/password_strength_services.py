from wtforms.validators import ValidationError
import re


def password_strength(form, field):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}$"
    if not re.match(pattern, field.data):
        raise ValidationError(
            "Slaptažodis privalo turėti 8-20 simbolių, bent vieną mažą, didžiąją raidę ir skaičių."
        )
