from models.users import Users, db
from werkzeug.security import check_password_hash
from sqlalchemy import and_


def user_exists(email, password, role):
    user = db.session.execute(
        db.select(Users).filter(and_(Users.email == email, Users.role == role))
    ).scalar()
    if user and check_password_hash(user.password, password):
        return user
