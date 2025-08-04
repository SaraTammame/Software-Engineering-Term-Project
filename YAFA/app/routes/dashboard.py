from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from app.routes import login_required
from app import db

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
@login_required
def dashboard():
    from datetime import datetime, timedelta
    from app.model.workout import Workout
    from app.model.journal import Journal

    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)

    workout_count = Workout.query.filter(
        Workout.user_id == g.user.id, Workout.workout_date >= week_ago.date()
    ).count()
    journal_count = Journal.query.filter(
        Journal.user_id == g.user.id, Journal.entry_date >= week_ago.date()
    ).count()

    recent_journals = (
        Journal.query.filter_by(user_id=g.user.id)
        .order_by(Journal.entry_date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        workout_count=workout_count,
        journal_count=journal_count,
        recent_journals=recent_journals,
    )
