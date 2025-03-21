from models.admin import Admin
from extensions import db


def admin_exists():
    admin = db.session.execute(db.select(Admin)).scalars().all()
    return admin
