from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.model.user import User
from app.model.workout import Workout
from app.model.journal import Journal
from app.model.model_example import test_insert
from app.model.workout import add_workout

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
    users = User.query.all()
    entry = Journal.query.all()
    if request.method == "POST":
        try:
            user_id = int(request.form["user_id"])
            entry_date = request.form["entry_date"]
            entry_title = request.form["entry_title"]
            entry_content = request.form["entry_content"]
        except ValueError:
            error_message = "Invalid input: Please enter valid numbers for ID."
        else:
            user = User.query.get(user_id)
            if user is None:
                error_message = f"User with ID {user_id} does not exist."
            else:
                new_entry = Journal(
                    user_id=user_id,
                    entry_date=entry_date,
                    entry_title=entry_title,
                    entry_content=entry_content,
                )
                db.session.add(new_entry)
                db.session.commit()
                return redirect(url_for("user.journal"))
    return render_template(
        "journal.html", user_query_result=users, journal_query_result=entry
    )


def add_journal_entry():

    return render_template("journal.html")


@user_bp.route("/data_base_test", methods=["GET"])
def data_base_test():
    test_insert()
    users = User.query.all()
    workouts = Workout.query.all()
    return render_template(
        "data_base_test.html",
        user_query_result=users,
        workout_query_result=workouts,
    )


@user_bp.route("/add_workout", methods=["GET", "POST"])
def add_workout_page():
    error_message = None
    if request.method == "POST":
        try:
            workout_id_str = request.form.get("workout_id")
            user_id = int(request.form["user_id"])
            workout_date = request.form["workout_date"]
            workout_type = request.form["workout_type"]
            workout_duration = int(request.form["workout_duration"])
            workout_distance = float(request.form["workout_distance"])
            workout_calories = int(request.form["workout_calories"])
            workout_notes = request.form["workout_notes"]
            workout_id = int(workout_id_str) if workout_id_str else None
        except ValueError:
            error_message = "Invalid input: Please enter valid numbers for ID, duration, distance, and calories."
        else:
            user = User.query.get(user_id)
            if user is None:
                error_message = f"User with ID {user_id} does not exist."
            elif workout_id is not None and Workout.query.get(workout_id):
                error_message = f"Workout with ID {workout_id} already exists."
            else:
                add_workout(
                    user_id,
                    workout_date,
                    workout_type,
                    workout_duration,
                    workout_distance,
                    workout_calories,
                    workout_notes,
                    workout_id=workout_id,
                )
                return redirect(url_for("user.add_workout_page"))
    workouts = Workout.query.all()
    return render_template(
        "add_workout.html", workout_query_result=workouts, error_message=error_message
    )


@user_bp.route("/progress", methods=["GET"])
def progress():
    workouts = Workout.query.order_by(Workout.workout_date).all()
    dates = [w.workout_date.strftime("%Y-%m-%d") for w in workouts]
    durations = [w.workout_duration for w in workouts]
    return render_template("progress.html", dates=dates, durations=durations)


# register the blueprint
def register_blueprints(app):
    app.register_blueprint(user_bp)
