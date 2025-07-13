from app import db
from app.model.workout import Workout


def add_workout(
    user_id,
    workout_date,
    workout_type,
    workout_duration,
    workout_distance,
    workout_calories,
    workout_notes,
    workout_id=None,
):
    kwargs = {
        "user_id": user_id,
        "workout_date": workout_date,
        "workout_type": workout_type,
        "workout_duration": workout_duration,
        "workout_distance": workout_distance,
        "workout_calories": workout_calories,
        "workout_notes": workout_notes,
    }
    if workout_id is not None:
        kwargs["id"] = workout_id
    obj = Workout(**kwargs)
    db.session.add(obj)
    db.session.commit()
