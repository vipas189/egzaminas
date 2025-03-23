from extensions import db


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)
    points = db.Column(db.Float, nullable=False)

    # ForeignKeys
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"), nullable=False)

    # Relationships
    answers = db.relationship(
        "Answers", backref="questions", cascade="all, delete-orphan"
    )
