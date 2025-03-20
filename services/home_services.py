from models.users import Users
from extensions import db


def admin_exists():
    admin = db.session.execute(db.select(Users)).scalars().all()
    return admin
