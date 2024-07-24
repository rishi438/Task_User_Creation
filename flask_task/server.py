from flask import make_response, render_template, request

from flask_task.api.route_handler import api_routes
from flask_task.app_build import create_app

app, jwt = create_app()


with app.app_context():
    app.register_blueprint(api_routes, url_prefix="/api")


@app.route("/test", methods=["GET"])
def test():
    """_summary_

    Returns:
        _type_: _description_
    """
    data = {"name": "UP and Running."}
    return make_response(render_template("/layouts/index.html", **data), 200)


@app.route("/login", methods=["GET"])
def login():
    """_summary_

    Returns:
        _type_: _description_
    """
    return make_response(render_template("/pages/login.html"), 200)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """_summary_

    Returns:
        _type_: _description_

    """
    data = {}
    data["username"] = request.args.get("username")
    return make_response(render_template("/pages/dashboard.html", **data), 200)


if __name__ == "__main__":
    app.debug = True
    app.run()
