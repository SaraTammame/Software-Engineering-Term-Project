from app import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # store hashed passwords, so allocate generous length
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Link to any workout names this user has created themselves
    custom_workout_names = db.relationship(
        "WorkoutName", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }


def insert_user_data(id, username, password, email="test@example.com"):
    """Utility used by tests/sample scripts to insert users quickly.

    Passwords are hashed to match production behaviour.
    """
    # Accept only signed 32-bit integer primary keys for now.
    MAX_INT32 = 2**31 - 1
    if not isinstance(id, int) or id < 0 or id > MAX_INT32:
        raise ValueError(
            f"id must be a signed 32-bit integer (0 – {MAX_INT32}); got {id}"
        )

    if not User.query.filter_by(id=id).first():
        obj = User(
            id=id,
            username=username,
            password=generate_password_hash(password),
            email=email.lower(),
        )
        db.session.add(obj)

    db.session.commit()
