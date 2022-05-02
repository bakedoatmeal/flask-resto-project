from .models import User
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.extensions import app, db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)