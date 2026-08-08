"""
AI Career Connect - Application Factory

This __init__.py uses the Flask Application Factory pattern.
It creates and configures the Flask app, initializes extensions
(SQLAlchemy, Login Manager), and registers all Blueprints.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config_by_name

# ------------------------------------
# Extension instances (shared globally)
# ------------------------------------

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app(config_name="development"):
    """
    Application Factory function.
    Creates a Flask app, loads config, initializes extensions,
    and registers blueprints.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # ---- Register Blueprints ----
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.resume import resume_bp
    from app.routes.interview import interview_bp
    from app.routes.roadmap import roadmap_bp
    from app.routes.speech import speech_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(speech_bp)

    # ---- Root Route ----
    @app.route("/")
    def root():
        from flask import redirect, url_for
        return redirect(url_for("dashboard.index"))

    # Create database tables
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app