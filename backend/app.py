from flask import Flask
from backend.routes import main_routes
from backend.models import db, User
from datetime import timedelta
from werkzeug.security import generate_password_hash
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static",
    instance_relative_config=True
)

app.secret_key = "vts_super_secret_key_2026"
app.permanent_session_lifetime = timedelta(minutes=30)

# load database config
app.config.from_pyfile("../config.py")

db.init_app(app)
app.register_blueprint(main_routes)

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password=generate_password_hash("admin123")
        )
        db.session.add(admin)
        db.session.commit()

    print("DB =", app.config["SQLALCHEMY_DATABASE_URI"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
