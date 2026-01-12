from flask import Flask
from backend.routes import main_routes
from backend.config import Config
from backend.models import db, User
from datetime import timedelta
from werkzeug.security import generate_password_hash

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Secret key (stable)
app.secret_key = "vts_super_secret_key_2026"

# Load config class
app.config.from_object(Config)

# Session
app.permanent_session_lifetime = timedelta(minutes=30)

# Init DB
db.init_app(app)

# Register routes
app.register_blueprint(main_routes)

# Create DB + ensure admin
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password=generate_password_hash("admin123"))
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run()
