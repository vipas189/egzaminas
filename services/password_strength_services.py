from wtforms.validators import ValidationError
import re


def password_strength(form, field):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
    if not re.match(pattern, field.data):
        raise ValidationError(
            "Slatpazodis privalo buti 8 simboliu ilgio, turi tureti bent viena maza raide, didziaji raide ir skaiciu."
        )
