from app import db


class Workout(db.Model):
    __tablename__ = "workout"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    workout_date = db.Column(db.Date, nullable=False)
    workout_type = db.Column(db.String(80), nullable=False)
    workout_duration = db.Column(db.Integer, nullable=False)
    workout_distance = db.Column(db.Float, nullable=False)
    workout_calories = db.Column(db.Integer, nullable=False)
    workout_notes = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "workout_date": self.workout_date,
            "workout_type": self.workout_type,
            "workout_duration": self.workout_duration,
            "workout_distance": self.workout_distance,
            "workout_calories": self.workout_calories,
            "workout_notes": self.workout_notes,
        }
