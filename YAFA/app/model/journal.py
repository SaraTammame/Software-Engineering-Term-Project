from app import db

# Association table to link many workouts to many journal entries
journal_workout_association = db.Table(
    "journal_workout_association",
    db.Column("journal_id", db.Integer, db.ForeignKey("journal.id"), primary_key=True),
    db.Column("workout_id", db.Integer, db.ForeignKey("workout.id"), primary_key=True),
)


class Journal(db.Model):
    __tablename__ = "journal"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    entry_title = db.Column(db.String(255), nullable=False)
    entry_content = db.Column(db.Text, nullable=False)

    # Workouts linked to this journal entry (many-to-many)
    workouts = db.relationship(
        "Workout",
        secondary=journal_workout_association,
        back_populates="journals",
    )

    def __repr__(self):
        return f"<JournalEntry {self.entry_title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "entry_date": self.entry_date,
            "entry_title": self.entry_title,
            "entry_content": self.entry_content,
            "workout_ids": [w.id for w in self.workouts],
        }
