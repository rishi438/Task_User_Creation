from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from flask_task.api.models import db
from flask_task.utils.environment import (
    DATABASE_URI,
    JWT_SECRET_KEY,
    TEMPLATES_AUTO_RELOAD,
)


def create_app():
    """
    Create and configure the Flask application.
    Parameters:
        - None
    Returns:
        - tuple: A tuple containing the Flask app and initialized JWTManager.
    Example:
        - create_app() -> (Flask app, JWTManager)
    """
    app = Flask(__name__)

    config = {
        "TEMPLATES_AUTO_RELOAD": TEMPLATES_AUTO_RELOAD,
        "SQLALCHEMY_DATABASE_URI": DATABASE_URI,
        "JWT_SECRET_KEY": JWT_SECRET_KEY,
        "JWT_COOKIE_SECURE": False,
        "JWT_COOKIE_CSRF_PROTECT": False,
        "JWT_TOKEN_LOCATION": ["cookies"],
        "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=2),
    }

    app.config.update(config)

    jwt = JWTManager(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app, jwt
