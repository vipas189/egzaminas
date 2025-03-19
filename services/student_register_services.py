from models.users import Users
from extensions import db


def student_exists():
    students = db.session.execute(db.select(Users)).scalars().all()
    return students
