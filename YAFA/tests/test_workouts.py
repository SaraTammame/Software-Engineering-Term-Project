from datetime import date
import pytest
from app.model.workout import add_workout, Workout
from app.model.user import insert_user_data
from sqlalchemy.exc import IntegrityError


def test_add_workout_with_existing_user_id(app):
    """
    TC-WORKOUT-001:
    Ensure adding a workout with an existing user_id succeeds.
    """
    valid_user_id = 1
    insert_user_data(valid_user_id, "test", "test")

    workout_id = 1
    workout_date = date(2025, 1, 1)
    workout_type = "test"
    workout_duration = 10
    workout_distance = 10
    workout_calories = 100
    workout_notes = "test"

    add_workout(
        valid_user_id,
        workout_date,
        workout_type,
        workout_duration,
        workout_distance,
        workout_calories,
        workout_notes,
        workout_id,
    )

    with app.app_context():
        assert Workout.query.filter_by(id=workout_id).first() is not None


def test_add_workout(app):
    """
    TC-WORKOUT-001:
    Ensure adding a workout with a non-existent user_id raises ValueError.
    """
    valid_user_id = 1
    insert_user_data(valid_user_id, "test", "test")

    workout_id = 1
    workout_date = date(2025, 1, 1)
    workout_type = "test"
    workout_duration = 10
    workout_distance = 10
    workout_calories = 100
    workout_notes = "test"

    add_workout(
        valid_user_id,
        workout_date,
        workout_type,
        workout_duration,
        workout_distance,
        workout_calories,
        workout_notes,
        workout_id,
    )

    nonexistent_user_id = 9999
    with app.app_context(), pytest.raises(IntegrityError):
        add_workout(
            nonexistent_user_id,
            workout_date,
            workout_type,
            workout_duration,
            workout_distance,
            workout_calories,
            workout_notes,
            workout_id + 1,
        )
