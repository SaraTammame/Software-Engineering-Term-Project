from flask import Blueprint, request, jsonify, g
from app import db
from app.model.workout import Workout
from app.routes import login_required

bp = Blueprint("location", __name__)

@bp.route("/save_location", methods=["POST"])
@login_required
def save_location():
    data = request.get_json()
    lat = data.get("latitude")
    lon = data.get("longitude")
    workout_id = data.get("workout_id")

    if not lat or not lon or not workout_id:
        return jsonify({"error": "Missing data"}), 400

    workout = Workout.query.filter_by(id=workout_id, user_id=g.user.id).first()
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    workout.workout_location = f"{lat}, {lon}"
    db.session.commit()

    return jsonify({"message": "Location saved successfully"})
