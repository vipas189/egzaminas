from wtforms.validators import ValidationError
import re


def name_strength(form, field):
    if not re.match(r"^[a-zA-Z]{2,}$", field.data):
        raise ValidationError(
            "Vardas neatitinka formato ar susideda iš mažiau nei 2 simbolių."
        )


def last_name_strength(form, field):
    if not re.match(r"^[a-zA-Z]{2,}$", field.data):
        raise ValidationError(
            "Pavardė neatitinka formato ar susideda iš mažiau nei 2 simbolių."
        )


def email_strength(form, field):
    pattern = r"^(?!.*\.\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, field.data):
        raise ValidationError("Neteisingas el. pašto formatas. ")


def password_strength(form, field):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}$"
    if not re.match(pattern, field.data):
        raise ValidationError(
            "Slaptažodis privalo turėti 8-20 simbolių, bent vieną mažą, didžiąją raidę ir skaičių."
        )
