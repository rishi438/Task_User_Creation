from datetime import timedelta

from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
)

from flask_task.api.models import Task, User, db
from flask_task.utils.constants import API_RESPONSE_OBJ, UserType

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
        username = data.get("username", None)
        password = data.get("password", None)
        if username and password:
            user = User()
            user = User.query.filter_by(username=username.lower()).first()
            if user is None:
                response["msg"] = "User does not exist"
                return jsonify(response)
            pass_check = user.check_password(password)
            if pass_check:
                access_token = access_token = create_access_token(
                    identity=user.username, expires_delta=timedelta(hours=1)
                )
                response["status"] = True
                response["msg"] = "Logged In Successfully"
                resp = make_response(jsonify(response))
                set_access_cookies(resp, access_token)
                return resp
            response["msg"] = "Missing username or password"
        else:
            response["msg"] = "Invalid password"
    except Exception as ex:
        print(f"Error Occurred route_handler.user_login: {ex}")
    return make_response(jsonify(response))


@api_routes.route("/users", methods=["GET"])
@jwt_required(locations=["cookies"])
def user_data():
    """_summary_

    Returns:
        _type_: _description_
    """
    response = API_RESPONSE_OBJ.copy()
    response["msg"] = "Error Occured!"
    try:
        # user_id = get_jwt_identity()
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


@api_routes.route("/add-task", methods=["POST"])
@jwt_required(locations=["cookies"])
def add_task():
    """_summary_

    Returns:
        _type_: _description_
    """
    response = API_RESPONSE_OBJ.copy()
    response["msg"] = "Error Occured!"
    try:
        data = request.get_json() or {}

        username = get_jwt_identity()
        created_for_username = data.get("created_for", None)
        user = User.query.filter_by(username=username.lower()).first()
        if UserType(user.role).name == "ADMIN" and created_for_username:
            created_for = User.query.filter_by(
                username=created_for_username.lower()
            ).first()
            task_data = data.get("task_data", {})
            task_data["created_user"] = user.user_id
            task_data["created_for"] = created_for.user_id
            if (
                task_data
                and task_data.get("created_user", None)
                and task_data.get("status", None)
            ):
                task = Task(**task_data)
                if task:
                    db.session.add(task)
                    db.session.commit()
                    response["msg"] = "Task Created Successfully"
                    response["status"] = True
                else:
                    response["msg"] = (
                        "Task Creation Failed! Try again sometime"
                    )
            else:
                response["msg"] = "Missing Fields!"
        else:
            response["msg"] = (
                "You don't have enough privilages to publish task"
            )
    except Exception as ex:
        print(f"Error Occured add_task: {ex}")
    return make_response(jsonify(response))
