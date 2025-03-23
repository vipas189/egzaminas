from extensions import db


class Tests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    time_limit = db.Column(db.Integer)  # Minutes allowed
    passing_score = db.Column(db.Float)
    is_exam = db.Column(db.Boolean, default=False)

    # ForeignKeys
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)

    # Relationships
    module = db.relationship("Modules", backref="tests")
    questions = db.relationship(
        "Questions", backref="tests", cascade="all, delete-orphan"
    )
