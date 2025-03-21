from wtforms.validators import ValidationError
import re


def email_strength(form, field):
    pattern = r"^(?!.*\.\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, field.data):
        raise ValidationError("Neteisingas el.pašto adresas")
