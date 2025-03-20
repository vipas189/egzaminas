from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # registracija studentui ir dest
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))

    role = db.Column(db.String(20), nullable=False)  # 'adminas', 'destytojas', 'studentas'
    is_main_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    
    def __init__(self, email, password, role, first_name=None, last_name=None, is_main_admin=False):
        self.email = email
        self.set_password(password)
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.is_main_admin = is_main_admin
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Vartotojas {self.email}>'
