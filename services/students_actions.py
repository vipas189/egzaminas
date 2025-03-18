from models.student import Student
from extensions import db

def view_students():
    students = db.session.execute(db.select(Student)).scalars().all()
    return students