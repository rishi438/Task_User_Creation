from flask import Flask

from flask_task.api.models import db
from flask_task.utils.environment import (
    DATABASE_URI,
    TEMPLATES_AUTO_RELOAD
)


def create_app():
    """Creates Web Server Application

    Returns:
        tuple: containing instances of app and celery
    """

    app = Flask(__name__)

    app.config["TEMPLATES_AUTO_RELOAD"] = TEMPLATES_AUTO_RELOAD
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
