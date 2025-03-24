from models.users import Users, db
from werkzeug.security import check_password_hash


def admin_exists(email, password):
    admin = db.session.execute(db.select(Users).filter_by(email=email)).scalar_one_or_none()
    if admin and check_password_hash(admin.password, password):
        return admin

def add_admin(email, password_hash, name=None, last_name=None):

    admin = Users(
        email=email,
        password=password_hash,
        name=name,
        last_name=last_name
    )
    db.session.add(admin)
    db.session.commit()
    return admin