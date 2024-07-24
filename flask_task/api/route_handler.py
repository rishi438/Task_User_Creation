from datetime import datetime, timedelta

from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token  # get_jwt_identity,
from flask_jwt_extended import jwt_required

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
            access_token = access_token = create_access_token(
                identity="user_id", expires_delta=timedelta(hours=1)
            )
            expires = datetime.now() + timedelta(hours=1)
            response["status"] = True
            response["msg"] = "Logged In Successfully"
            resp = make_response(jsonify(response))
            resp.set_cookie(
                "access_token", access_token, httponly=True, expires=expires
            )
            return resp
        else:
            response["msg"] = "Invalid password"
    except Exception as ex:
        print(f"Error Occurred route_handler.user_login: {ex}")
    return make_response(jsonify(response))


@api_routes.route("/users", methods=["GET"])
@jwt_required()
def user_data():
    try:
        # user_id = get_jwt_identity()
        response = API_RESPONSE_OBJ.copy()
        response["msg"] = "Error Occured!"
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({"username": user.username, "role": user.role})
        response["status"] = True
        response["msg"] = "Users retrieved successfully"
        response["data"] = {}
        response["data"]["users"] = user_list
    except Exception as ex:
        print(f"Error Occured user_data: {ex}")
    return make_response(jsonify(response))
