from app import db
from app.model.user import User


def test_insert():

    sample_users = [
        {"id": 1, "username": "harry"},
        {"id": 2, "username": "trican"},
        {"id": 3, "username": "minh"},
        {"id": 4, "username": "sara"},
    ]

    for entry in sample_users:
        if not User.query.filter_by(id=entry["id"]).first():
            obj = User(**entry)
            db.session.add(obj)

    db.session.commit()
