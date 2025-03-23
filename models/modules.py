from extensions import db


class Modules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)  # Academic year
    schedule = db.Column(db.Text)  # Could be JSON or structured text with schedule info

    # ForeignKeys
    study_program_id = db.Column(db.Integer, db.ForeignKey("study_programs.id"))

    # Relationships
    study_program = db.relationship("StudyPrograms", backref="modules")
    prerequisites = db.relationship(
        "Modules",
        secondary="module_prerequisites",
        primaryjoin="Modules.id==module_prerequisites.c.module_id",
        secondaryjoin="Modules.id==module_prerequisites.c.prerequisite_id",
        backref="required_for",
    )
