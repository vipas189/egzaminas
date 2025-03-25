from models.users import Users
from extensions import db
from werkzeug.security import check_password_hash


def admin_exists(email, password):
    admin = db.session.execute(db.select(Users).filter_by(email=email)).scalar_one_or_none()
    if admin and check_password_hash(admin.password, password):
        return admin

