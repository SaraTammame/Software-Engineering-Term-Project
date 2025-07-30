from app import db
from datetime import datetime, date
from app.model.journal import journal_workout_association  # import association table


class Workout(db.Model):
    __tablename__ = "workout"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Optional foreign-key to the name catalogue; keeps existing fallback string
    name_id = db.Column(db.Integer, db.ForeignKey("workout_name.id"), nullable=True)
    workout_name = db.relationship("WorkoutName", back_populates="workouts")

    workout_date = db.Column(db.Date, nullable=False)

    # Keep the free-text column for now to avoid breaking current flows
    workout_type = db.Column(db.String(80), nullable=False)

    workout_duration = db.Column(db.Integer, nullable=False)
    workout_distance = db.Column(db.Float, nullable=False)
    workout_calories = db.Column(db.Integer, nullable=False)
    workout_notes = db.Column(db.String(255), nullable=True)

    # Back-reference to journal entries
    journals = db.relationship(
        "Journal",
        secondary=journal_workout_association,
        back_populates="workouts",
    )

    def __repr__(self):
        return f"<Workout {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name_id": self.name_id,
            "workout_date": self.workout_date,
            "workout_type": self.workout_type,
            "workout_duration": self.workout_duration,
            "workout_distance": self.workout_distance,
            "workout_calories": self.workout_calories,
            "workout_notes": self.workout_notes,
        }


# existing helper functions unchanged...


def _coerce_date(value):
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError(
                "workout_date must be YYYY-MM-DD or datetime.date"
            ) from exc
    raise TypeError("workout_date must be str or datetime.date")


def add_workout(
    user_id,
    workout_date,
    workout_type,
    workout_duration,
    workout_distance,
    workout_calories,
    workout_notes,
    workout_id=None,
    name_id=None,
):

    kwargs = {
        "user_id": user_id,
        "workout_date": _coerce_date(workout_date),
        "workout_type": workout_type,
        "workout_duration": workout_duration,
        "workout_distance": workout_distance,
        "workout_calories": workout_calories,
        "workout_notes": workout_notes,
    }
    if workout_id is not None:
        kwargs["id"] = workout_id
    if name_id is not None:
        kwargs["name_id"] = name_id

    obj = Workout(**kwargs)
    db.session.add(obj)
    db.session.commit()
