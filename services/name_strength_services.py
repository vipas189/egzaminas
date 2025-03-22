from wtforms.validators import ValidationError
import re


def name_strength(form, field):
    if not re.match(r"^[a-zA-Z]{2,}$", field.data):
        raise ValidationError(
            "Vardas neatitinka formato ar susideda iš mažiau nei 2 simbolių."
        )
