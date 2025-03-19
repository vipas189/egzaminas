from extensions import db
from datetime import datetime

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    weight = db.Column(db.Float)  # Percentage weight in the final grade
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Assessment {self.title}>'