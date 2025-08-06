from app import db

class NotificationPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reminder_type = db.Column(db.String(80), nullable=False)  # e.g., 'email', 'sms'
    times = db.Column(db.String, nullable=False)  # CSV times, e.g., "08:00,12:00"
    message = db.Column(db.String, nullable=False)
    email_enabled = db.Column(db.Boolean, default=True)  # enable/disable email notifications

    def __repr__(self):
        return f"<NotificationPreference {self.reminder_type} for user {self.user_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "reminder_type": self.reminder_type,
            "times": self.times.split(","),
            "message": self.message,
            "email_enabled": self.email_enabled,
        }
