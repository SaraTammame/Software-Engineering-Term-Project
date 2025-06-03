from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # from flask quickstart guide
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/<name>")
    def hello(name):
        return render_template("template.html", name=name)

    return app 