from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from app import db
from app.model.user import User
from app.model.workout import Workout, add_workout
from app.model.workout_name import WorkoutName
from sqlalchemy import func
from app.model.journal import Journal

# Create a Blueprint named 'user'
user_bp = Blueprint("user", __name__)


# ---------------------------
# Pages
# ---------------------------
@user_bp.route("/")
def home():
    return render_template("home.html")


@user_bp.route("/insert", methods=["POST"])
def insert_sample_rows():
    test_insert()
    return render_template("insert.html")


@user_bp.route("/auth", methods=["GET", "POST"])
def auth():
    error_message = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = User.query.filter_by(username=username).first()
        if user is None:
            error_message = "Invalid username."
        elif user.password != password:
            error_message = "Invalid password."
        else:
            # Successful login: you can set session/cookies here if needed
            return redirect(url_for("user.home"))
    return render_template("login.html", error_message=error_message)


@user_bp.route("/journal", methods=["POST", "GET"])
def journal():
    current_uid = session.get("current_uid")
    if current_uid is None:
        return redirect(url_for("user.login", next=request.path))

    users = User.query.all()
    entry = Journal.query.filter_by(user_id=current_uid).all()
    error_message = None

    if request.method == "POST":
        try:
            entry_date = request.form["entry_date"]
            entry_title = request.form["entry_title"]
            entry_content = request.form["entry_content"]
        except KeyError:
            error_message = "Missing form fields."
        else:
            new_entry = Journal(
                user_id=current_uid,
                entry_date=entry_date,
                entry_title=entry_title,
                entry_content=entry_content,
            )
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for("user.journal"))

    return render_template(
        "journal.html",
        user_query_result=users,
        journal_query_result=entry,
        current_uid=current_uid,
        error_message=error_message,
    )


@user_bp.route("/add_workout", methods=["GET", "POST"])
def add_workout_page():
    current_uid = session.get("current_uid")
    if current_uid is None:
        return redirect(url_for("user.login", next=request.path))

    error_message = None

    if request.method == "POST":
        try:
            workout_date = request.form["workout_date"]
            typed_name = request.form["workout_type"].strip()
            workout_duration = int(request.form["workout_duration"])
            workout_distance = float(request.form["workout_distance"])
            workout_calories = int(request.form["workout_calories"])
            workout_notes = request.form["workout_notes"]
        except ValueError:
            error_message = "Invalid numbers provided."
        else:
            # Find or create workout_name entry (global or user-specific)
            name_obj = WorkoutName.query.filter(
                func.lower(WorkoutName.name) == typed_name.lower(),
                (
                    (WorkoutName.user_id.is_(None))
                    | (WorkoutName.user_id == current_uid)
                ),
            ).first()
            if name_obj is None:
                name_obj = WorkoutName(name=typed_name, user_id=current_uid)
                db.session.add(name_obj)
                db.session.commit()  # commit so we get its ID

            add_workout(
                current_uid,
                workout_date,
                typed_name,
                workout_duration,
                workout_distance,
                workout_calories,
                workout_notes,
                name_id=name_obj.id,
            )
            return redirect(url_for("user.add_workout_page"))

    workouts = Workout.query.filter_by(user_id=current_uid).all()
    name_rows = (
        WorkoutName.query.filter(
            (WorkoutName.user_id.is_(None)) | (WorkoutName.user_id == current_uid)
        )
        .order_by(WorkoutName.name)
        .all()
    )
    workout_names = [n.name for n in name_rows]

    return render_template(
        "add_workout.html",
        workout_query_result=workouts,
        error_message=error_message,
        current_uid=current_uid,
        workout_names=workout_names,
    )


@user_bp.route("/progress")
def progress():
    current_uid = session.get("current_uid")
    if current_uid is None:
        return redirect(url_for("user.login", next=request.path))

    workouts = (
        Workout.query.filter_by(user_id=current_uid)
        .order_by(Workout.workout_date)
        .all()
    )
    dates = [w.workout_date.strftime("%Y-%m-%d") for w in workouts]
    durations = [w.workout_duration for w in workouts]
    return render_template("progress.html", dates=dates, durations=durations)


@user_bp.route("/workout/<int:workout_id>")
def workout_detail(workout_id):
    current_uid = session.get("current_uid")
    if current_uid is None:
        return redirect(url_for("user.login", next=request.path))

    workout = Workout.query.filter_by(id=workout_id, user_id=current_uid).first_or_404()
    return render_template("workout_detail.html", workout=workout)


# register the blueprint
def register_blueprints(app):
    app.register_blueprint(user_bp)
