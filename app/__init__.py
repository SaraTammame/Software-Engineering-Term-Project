from flask import Flask, render_template
from flask_pymongo import PyMongo
from app.models import test_insert, test_query

def create_app():
    app = Flask(__name__)

    try:
        from config import Config
        mongo_uri = Config.MONGO_URI
    except ImportError:
        raise ValueError("MONGO_URI not found in config.py")
    
    app.config["MONGO_URI"] = mongo_uri
    mongo = PyMongo(app)
    app.mongo = mongo

    # from flask quickstart guide
    @app.route("/")
    def hello_world():
        test_insert(app.mongo)
        return render_template("test_greeting.html")

    @app.route("/test_query")
    def hello():
        query_result =test_query(app.mongo)
        return render_template("test_query.html", query_result=query_result)

    return app 