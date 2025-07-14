from app import db

class Journal(db.Model):
    __tablename__ = "journal"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    entry_title = db.Column(db.String(255), nullable=False)
    entry_content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<JournalEntry {self.entry_title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "entry_date": self.entry_date,
            "entry_title": self.entry_title,
            "entry_content": self.entry_content,
        }
