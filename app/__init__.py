from flask import Flask, render_template
from flask_pymongo import PyMongo
from app.models import test_insert, test_query

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = "mongodb+srv://hachoj:yJsUEtLxpnqobesK@yafa-db.yvwbol0.mongodb.net/flask_app?retryWrites=true&w=majority&appName=yafa-db"
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