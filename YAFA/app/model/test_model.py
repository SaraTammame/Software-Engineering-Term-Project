from app import db
from app.model.user import User


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

    db.session.commit()
