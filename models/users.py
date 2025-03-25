from extensions import db
from flask_login import UserMixin
 
 
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    profile_picture = db.Column(db.String(255), default='uploads/profile_stock.jpg')
 
    # Security
    login_attempts = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime)
    suspended_until = db.Column(db.DateTime)
 
    # ForeignKeys
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    # group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
 
    # Relationships
    program = db.relationship("Program", backref="users")
    # group = db.relationship("Groups", backref="users")