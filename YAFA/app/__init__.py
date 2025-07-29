from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Configure your database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the extension with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # register the blueprints
    from app.routes import user_routes

    user_routes.register_blueprints(app)

    # from app.notifications.notifications import init_notifications

    # init_notifications(app)

    return app
