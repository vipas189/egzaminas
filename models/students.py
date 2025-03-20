from extensions import db


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    study_program = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))
