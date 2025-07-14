from flask import Blueprint, render_template
from app.model.user import User
from app.model.test_model import test_insert

# Create a Blueprint named 'user'
user_bp = Blueprint("user", __name__)


# # Define routes for this blueprint
# @user_bp.route("/users", methods=["GET"])
# def get_users():
#     # This route uses the User model to get data from database
#     users = User.query.all()
#     return {"users": [user.to_dict() for user in users]}


@user_bp.route("/", methods=["POST", "GET"])
def home():
    # This route renders the home page
    return render_template("home.html")


@user_bp.route("/insert", methods=["POST"])
def insert_sample_rows():
    test_insert()
    return render_template("insert.html")


@user_bp.route("/users", methods=["GET"])
def get_users():
    # This route uses the User model to get data from database
    users = User.query.all()
    return render_template("users.html", users=users)


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # This route uses the User model to get a specific user
    user = User.query.get(user_id)
    if user:
        return user.to_dict()
    return {"error": "User not found"}, 404
