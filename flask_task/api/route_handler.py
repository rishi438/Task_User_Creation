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
    """
    Adds a new user to the database.
    Parameters:
        - None
    Returns:
        - dict: A JSON response object containing the status and message.
    Example:
        add_user() -> {"msg": "Added Successfully", "status": True}
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
            db.session.add(user)
            db.session.commit()
            response["msg"] = "Added Successfully"
            response["status"] = True
    except Exception as ex:
        print(f"Error Occurred route_handler.add_user: {ex}")

    return jsonify(response)


@api_routes.route("/login", methods=["POST"])
def user_login():
    """
    Handle user login and generate a response with an access token
    if credentials are valid.
    Parameters:
        - None
    Returns:
        - flask.Response: JSON response indicating login success or
        failure with appropriate message.
    user_login() -> {"status": bool, "msg": str}
        - Example input: {"username": "testuser", "password": "password123"}
        - Example output: {"status": True, "msg": "Logged In Successfully"}
    """
    response = API_RESPONSE_OBJ.copy()
    response["msg"] = "Error Occurred!"

    try:
        data = request.get_json() or {}
        username, password = data.get("username"), data.get("password")

        if not username or not password:
            response["msg"] = "Missing username or password"
            return make_response(jsonify(response))

        user = User.query.filter_by(username=username.lower()).first()

        if not user:
            response["msg"] = "User does not exist"
            return make_response(jsonify(response))

        if user.check_password(password):
            access_token = create_access_token(
                identity=user.username, expires_delta=timedelta(hours=1)
            )
            response["status"] = True
            response["msg"] = "Logged In Successfully"
            resp = make_response(jsonify(response))
            set_access_cookies(resp, access_token)
            return resp

        response["msg"] = "Invalid password"

    except Exception as ex:
        print(f"Error Occurred route_handler.user_login: {ex}")

    return make_response(jsonify(response))


@api_routes.route("/users", methods=["GET"])
@jwt_required(locations=["cookies"])
def user_data():
    """
    Fetches user data from the database and constructs a response object.
    Returns:
        - dict: JSON response containing the status, message, and
        user data, if applicable.
    user_data() -> {
        "status": True,
        "msg": "Users retrieved successfully",
        "data": {
            "users": [
                {"username": "sample_user", "role": "sample_role"},
                ...
            ]
        }
    }
        - This example assumes a successful retrieval of user data.
    """
    response = API_RESPONSE_OBJ.copy()
    response["msg"] = "Error Occurred!"

    try:
        # user_id = get_jwt_identity()
        users = User.query.all()
        user_list = [
            {"username": user.username, "role": user.role} for user in users
        ]

        response.update(
            {
                "status": True,
                "msg": "Users retrieved successfully",
                "data": {"users": user_list},
            }
        )
    except Exception as ex:
        print(f"Error Occurred user_data: {ex}")

    return make_response(jsonify(response))


@api_routes.route("/add-task", methods=["POST"])
@jwt_required(locations=["cookies"])
def add_task():
    """
    Handles the addition of a task to the system.
    Parameters:
        - None
    Returns:
        - dict: A dictionary containing the status of the operation
        and a message indicating success or failure.
    Example:
        add_task() -> {'msg': 'Task Created Successfully', 'status': True}
            - This example shows a successful task creation response.
    """
    response = API_RESPONSE_OBJ.copy()
    response["msg"] = "Error Occured!"
    try:
        data = request.get_json() or {}

        username = get_jwt_identity()
        created_for_username = data.get("created_for")
        user = User.query.filter_by(username=username.lower()).first()
        if UserType(user.role).name == "ADMIN" and created_for_username:
            created_for = User.query.filter_by(
                username=created_for_username.lower()
            ).first()
            task_data = data.get("task_data", {})
            task_data["created_user"] = user.user_id
            task_data["created_for"] = created_for.user_id
            if all(
                [
                    task_data,
                    task_data.get("created_user"),
                    task_data.get("status"),
                ]
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
