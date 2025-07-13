from flask import Blueprint, render_template
from app import db
from app.model.user import User
from app.model.test_model import test_insert

# Create a Blueprint named 'user'
user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")


@user_bp.route("/insert", methods=["POST"])
def insert_sample_rows():
    test_insert()
    return render_template("insert.html")


@user_bp.route("/auth", methods=["POST", "GET"])
def auth():
    return render_template("auth.html")


@user_bp.route("/journal", methods=["POST", "GET"])
def journal():
    return render_template("journal.html")


@user_bp.route("/data_base_test", methods=["GET"])
def data_base_test():
    test_insert()
    users = User.query.all()
    return render_template("data_base_test.html", query_result=users)


# register the blueprint
def register_blueprints(app):
    app.register_blueprint(user_bp)
