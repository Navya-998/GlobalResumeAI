from flask import Flask
import os

from config import Config
from extensions import db, bcrypt, login_manager

from routes.main import main
from routes.resume import resume
from routes.auth import auth

from models.user import User
from models.resume import Resume
from routes.blog import blog
from routes.admin import admin

print("Database Path:", os.path.abspath("resume.db"))

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

app.register_blueprint(main)
app.register_blueprint(resume)
app.register_blueprint(auth)
app.register_blueprint(blog)
app.register_blueprint(admin)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)