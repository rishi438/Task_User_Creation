from flask import make_response, render_template, request

from flask_cors import CORS
from flask_task.api.route_handler import api_routes
from flask_task.app_build import create_app

app, jwt = create_app()
cors = CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "http://localhost:5000",
            "supports_credentials": True,
        }
    },
)

with app.app_context():
    app.register_blueprint(api_routes, url_prefix="/api")


@app.route("/test", methods=["GET"])
def test():
    """
    Renders an HTML template with specified data and returns an HTTP response.
    Parameters:
        - None
    Returns:
        - flask.Response: HTTP response with rendered HTML template and
        status code 200.
    test() -> <Response 200>
        - This example returns an HTTP response with the rendered
        '/layouts/index.html' template and data containing
        {"name": "UP and Running."}.
    """
    data = {"name": "UP and Running."}
    return make_response(render_template("/layouts/index.html", **data), 200)


@app.route("/", methods=["GET"])
def login():
    """
    Renders the login page and returns an HTTP response.
    Parameters:
        None
    Returns:
        - Response: An HTTP response object containing the rendered
        login page template with a 200 status code.
    login() -> <Response [200]>
        - This example demonstrates that calling the function will
        return an HTTP response object with a rendered template for
        the login page and a status code of 200.
    """

    return make_response(render_template("/pages/login.html"), 200)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Render the dashboard page with the data received from the request.
    Parameters:
        - None
    Returns:
        - Response: HTML page of the dashboard with a status code of 200.
    Example:
        - dashboard() -> <Response 200>
    """

    data = {}
    data["username"] = request.args.get("username")

    return make_response(render_template("/pages/dashboard.html", **data), 200)


if __name__ == "__main__":
    app.debug = True
    app.run()
