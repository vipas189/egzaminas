from models.users import Users, db
from werkzeug.security import check_password_hash
from sqlalchemy import and_
from datetime import datetime, timedelta


def user_exists(email, password, role):
    user = db.session.execute(
        db.select(Users).filter(and_(Users.email == email, Users.role == role))
    ).scalar()
    if user and check_password_hash(user.password, password):
        user.login_attempts = 0
        db.session.commit()
        return user


def user_email_exists(email, role):
    user = db.session.execute(
        db.select(Users).filter(and_(Users.email == email, Users.role == role))
    ).scalar()
    return user


def user_failed_login(email, role):
    user = db.session.execute(
        db.select(Users).filter(and_(Users.email == email, Users.role == role))
    ).scalar()
    user.last_failed_login = datetime.now()
    user.login_attempts += 1
    db.session.commit()
    if user.login_attempts >= 3:
        user.suspended_until = user.last_failed_login + timedelta(minutes=1)
        db.session.commit()
        return user.login_attempts
    return user.login_attempts


def user_blocked(email, role):
    user = db.session.execute(
        db.select(Users).filter(and_(Users.email == email, Users.role == role))
    ).scalar()
    if (user and user.suspended_until) and (datetime.now() < user.suspended_until):
        return True
