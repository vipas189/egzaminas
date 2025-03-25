from extensions import db


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # e.g., IFIN-18-A
    year = db.Column(db.Integer, nullable=False)  # Enrollment year

    # ForeignKeys
    study_program_id = db.Column(db.Integer, db.ForeignKey("program.id"))

    # Relationships
    study_program = db.relationship("Program", backref="groups")
