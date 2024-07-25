from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from flask_task.utils.constants import TaskType, UserType

db = SQLAlchemy()


class User(db.Model):
    """User schema

    Args:
        db.Model (object): The base class for User model.
    """

    user_id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid4())
    )
    username = db.Column(db.String(36), unique=True, nullable=False)
    mobile_number = db.Column(db.String(36), nullable=True)
    role = db.Column(db.Enum(UserType), default=1)
    password_hash = db.Column(db.String(128), nullable=False)
    last_modified = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
    created_date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def set_password(self, password):
        """_summary_

        Args:
            password (_type_): _description_
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """_summary_

        Args:
            password (_type_): _description_

        Returns:
            _type_: _description_
        """
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    """_summary_

    Args:
        db (_type_): _description_
    """

    task_id = db.Column(
        db.String(36),
        primary_key=True,
        unique=True,
        default=lambda: str(uuid4()),
        nullable=False,
    )
    status = db.Column(db.Enum(TaskType), default=0)
    created_user = db.Column(
        db.String(36), db.ForeignKey("user.user_id"), nullable=False
    )
    created_for = db.Column(
        db.String(36), db.ForeignKey("user.user_id"), nullable=False
    )
    last_modified = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
    created_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
