from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
 
db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
login_manager = LoginManager()

login_manager.login_view = 'login'
login_manager.login_message = 'Prašome prisijungti norint pasiekti šį puslapį.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models.users import User
    return db.session.get(User, int(user_id))