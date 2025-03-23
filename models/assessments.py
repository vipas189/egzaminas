from extensions import db


class Assignments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    weight = db.Column(db.Float)  # Weight in final grade calculation

    # ForeignKeys
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)

    # Relationships
    module = db.relationship("Modules", backref="assignments")
