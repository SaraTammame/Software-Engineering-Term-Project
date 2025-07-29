from app import db


class NotificationPreference(
    db.Model
):  # many preferences to one user; each preference is for a certain notif type
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reminder_type = db.Column(db.String(80), nullable=False)
    times = db.Column(
        db.String, nullable=False
    )  # represent as csv strings, e.g, "08:00,12:00,18:00"
    message = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<NotificationPreference {self.reminder_type} for user {self.user_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "reminder_type": self.reminder_type,
            "times": self.times.split(","),
            "message": self.message,
        }
