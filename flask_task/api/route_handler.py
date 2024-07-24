from flask import Blueprint, jsonify, request

from flask_task.api.models import User, db
from flask_task.utils.constants import API_RESPONSE_OBJ

api_routes = Blueprint("api", __name__)


@api_routes.route("/add-user", methods=["POST"])
def add_user():
    """Adding user details

    Returns:
        object : returns operation details
    """
    response = API_RESPONSE_OBJ.copy()
    response["msg"] = "Error Occured!"
    try:
        data = request.get_json() or {}
        if data:
            data["username"] = data["username"].lower()
            password = data.pop("password")
            user = User(**data)
            user.set_password(password)
            if user:
                db.session.add(user)
                db.session.commit()
                response["msg"] = "Added Successfully"
                response["status"] = True
    except Exception as ex:
        print(f"Error Occurred route_handler.add_user: {ex}")
    return jsonify(response)


@api_routes.route("/login", methods=["POST"])
def user_login():
    """Adding user details

    Returns:
        object : returns operation details
    """
    response = API_RESPONSE_OBJ.copy()
    response["msg"] = "Error Occured!"
    try:
        data = request.get_json() or {}
        if "username" not in data or "password" not in data:
            response["msg"] = "Missing username or password"
            return jsonify(response)
        user = User()
        username = data["username"].lower()
        password = data["password"]
        user = User.query.filter_by(username=username).first()
        if user is None:
            response["msg"] = "User does not exist"
            return jsonify(response)
        pass_check = user.check_password(password)
        if pass_check:
            response["msg"] = "Logged In Successfully"
            response["status"] = True
        else:
            response["msg"] = "Invalid password"
    except Exception as ex:
        print(f"Error Occurred route_handler.user_login: {ex}")
    return jsonify(response)
