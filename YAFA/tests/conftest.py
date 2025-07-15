import pytest
import os
from app import create_app, db
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3


@pytest.fixture
def app():
    # Point DATABASE_URL env-var at an in-memory SQLite database.
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    # Create the Flask app *after* overriding the env var so the
    # SQLAlchemy engine is initialised with SQLite, not Postgres.
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    # Only for the builtin sqlite3 driver
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
