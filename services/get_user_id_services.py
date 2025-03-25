from extensions import db
from models.users import Users


def get_user_id(email):
    user = db.session.execute(db.select(Users).filter_by(email=email)).scalar()
    return user.id
