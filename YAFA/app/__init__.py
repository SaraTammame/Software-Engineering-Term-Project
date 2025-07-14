from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
# right now this will throw an error when ran
# from app.notifications.notifications import init_notifications

load_dotenv()

db = SQLAlchemy()
# migrate = Migrate()


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Configure your database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the extension with the app
    db.init_app(app)

#     migrate.init_app(app, db)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # basic home page
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/auth')
    def auth():
        return render_template('auth.html')
#     from app.routes import user_routes

    @app.route('/journal')
    def journal():
        return render_template('journal.html')
#     app.register_blueprint(user_routes.user_bp)

    # right now this won't work
    # init_notifications(app)

    return app
