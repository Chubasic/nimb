from os import environ
from flask import Flask
from flask_cors import CORS


def create_app() -> Flask:
    app = Flask(environ.get("FLASK_APP_NAME", "app"))
    app.debug = environ.get("FLASK_DEBUG", False)
    CORS(
        app, origins=[environ.get("CORS_ALLOWED_ORIGIN")], methods=["GET", "POST"]
    )
    return app
