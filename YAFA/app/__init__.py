from flask import Flask, render_template, jsonify, g, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import secrets


# right now this will throw an error when ran
# from app.notifications.notifications import init_notifications

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    from app.notifications import notifications_bp

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = "your-very-secret-key"

    # Configure your database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Secret key for sessions
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or secrets.token_hex(16)

    # Initialize the extension with the app
    db.init_app(app)
    migrate.init_app(app, db)

    

    # --- Import models so they are registered with SQLAlchemy metadata ---
    # NOTE: Importing *after* init_app prevents circular-import issues.
    with app.app_context():
        # Import order matters to avoid circular dependencies
        from app.model import user, journal, workout, workout_name  # noqa: F401
        from app.model.user import User
    
    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")

        if user_id is None:
            g.user = None
        else:
            g.user = User.query.get(user_id)

    # register the blueprints
    from app.routes import user_routes
    from app.routes import auth

    user_routes.register_blueprints(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(notifications_bp)
    # print(app.url_map)

    # from app.notifications.notifications import init_notifications

    # init_notifications(app)

    return app
