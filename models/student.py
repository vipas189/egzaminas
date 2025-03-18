from extensions import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)

