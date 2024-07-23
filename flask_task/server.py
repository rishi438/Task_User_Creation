from flask import make_response, render_template
from flask_task.app_build import create_app
from flask_task.api.route_handler import api_routes

app = create_app()


with app.app_context():
    app.register_blueprint(api_routes, url_prefix="/api")


@app.route("/test",methods=["GET"])
def home():
    data = {
        "name": "UP and Running."
    }
    return make_response(render_template("/layouts/index.html", **data), 200)


if __name__ == "__main__":
    app.debug = True
    app.run()
