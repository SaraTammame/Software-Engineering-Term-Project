from app import db
from app.model.user import User
from app.model.workout import Workout


def test_insert():

    sample_users = [
        {"id": 1, "username": "harry", "password": "123456"},
        {"id": 2, "username": "trican", "password": "123456"},
        {"id": 3, "username": "minh", "password": "123456"},
        {"id": 4, "username": "sara", "password": "123456"},
    ]

    for entry in sample_users:
        if not User.query.filter_by(id=entry["id"]).first():
            obj = User(**entry)
            db.session.add(obj)

    sample_workouts = [
        {
            "id": 1,
            "user_id": 1,
            "workout_date": "2025-01-01",
            "workout_type": "running",
            "workout_duration": 30,
            "workout_distance": 5,
            "workout_calories": 100,
            "workout_notes": "Good workout",
        },
        {
            "id": 2,
            "user_id": 2,
            "workout_date": "2025-01-02",
            "workout_type": "cycling",
            "workout_duration": 45,
            "workout_distance": 10,
            "workout_calories": 200,
            "workout_notes": "Great workout",
        },
        {
            "id": 3,
            "user_id": 3,
            "workout_date": "2025-01-03",
            "workout_type": "swimming",
            "workout_duration": 60,
            "workout_distance": 15,
            "workout_calories": 300,
            "workout_notes": "Excellent workout",
        },
        {
            "id": 4,
            "user_id": 4,
            "workout_date": "2025-01-04",
            "workout_type": "yoga",
            "workout_duration": 75,
            "workout_distance": 20,
            "workout_calories": 400,
            "workout_notes": "Perfect workout",
        },
    ]

    for entry in sample_workouts:
        if not Workout.query.filter_by(id=entry["id"]).first():
            obj = Workout(**entry)
            db.session.add(obj)

    db.session.commit()
