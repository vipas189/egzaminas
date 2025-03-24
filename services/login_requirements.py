from functools import wraps
from flask import redirect, url_for
from flask_login import current_user, login_required


def login_role_required(role):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                return redirect(url_for("home"))
            return f(*args, **kwargs)

        return decorated_function

    return decorator
