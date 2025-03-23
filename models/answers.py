from extensions import db


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    # ForeignKeys
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
