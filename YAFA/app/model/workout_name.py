from app import db


class WorkoutName(db.Model):
    """Catalogue of workout names.

    Rows with user_id = NULL are global (predefined) names.
    Rows with user_id set belong only to that user.
    """

    __tablename__ = "workout_name"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    # Unique per-user (NULL treated separately in most DBs)
    __table_args__ = (db.UniqueConstraint("user_id", "name"),)

    # Relationships
    user = db.relationship("User", back_populates="custom_workout_names")
    workouts = db.relationship(
        "Workout", back_populates="workout_name", cascade="all, delete-orphan"
    )

    def __repr__(self):
        scope = "global" if self.user_id is None else f"user {self.user_id}"
        return f"<WorkoutName {self.name!r} ({scope})>"
