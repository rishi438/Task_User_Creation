# Flask Task Management Application

This project is a task management application built using Flask, SQLAlchemy, and Flask-JWT-Extended for handling user authentication and authorization.

## Table of Contents

1. [Installation](#installation)
2. [Running the Application](#running-the-application)
3. [API Endpoints](#api-endpoints)
4. [Environment Variables](#environment-variables)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-repo/flask-task-app.git
    cd flask-task-app
    ```

2. **Install Poetry:**

    Poetry is a dependency management tool for Python. You can install it using the official installer.

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    For detailed instructions, refer to the [Poetry documentation](https://python-poetry.org/docs/#installing-with-the-official-installer).

3. **Install project dependencies:**

    Once Poetry is installed, you can use it to install the project dependencies.

    ```sh
    poetry install
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add the required environment variables. An example `.env` file is provided below:

    ```env
    DATABASE_URI=sqlite:///db.sqlite3
    JWT_SECRET_KEY=your_jwt_secret_key
    TEMPLATES_AUTO_RELOAD=True
    ```

## Running the Application

1. **Activate the virtual environment:**

    ```sh
    poetry shell
    ```

2. **Run the Flask application:**

    ```sh
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

- **POST /add-user**

    Add a new user.

    ```sh
    curl -X POST http://127.0.0.1:5000/add-user -H "Content-Type: application/json" -d '{
        "username": "example",
        "password": "examplepassword",
        "role": "User",
        "mobilenumber": "1234567890"
    }'
    ```

- **POST /login**

    Log in a user.

    ```sh
    curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{
        "username": "example",
        "password": "examplepassword"
    }'
    ```

- **GET /users**

    Get a list of all users.

    ```sh
    curl -X GET http://127.0.0.1:5000/users -H "Content-Type: application/json"
    ```

- **POST /add-task**

    Add a new task (requires JWT token).

    ```sh
    curl -X POST http://127.0.0.1:5000/add-task -H "Content-Type: application/json" -H "Authorization: Bearer <your_jwt_token>" -d '{
        "created_for": "user2",
        "task_data": {
            "title": "New Task",
            "description": "Task description",
            "status": "Pending"
        }
    }'
    ```

## Environment Variables

The following environment variables need to be set for the application to run correctly:

- **DATABASE_URI**: The URI for the database (e.g., `sqlite:///db.sqlite3`).
- **JWT_SECRET_KEY**: The secret key used for JWT token generation.
- **TEMPLATES_AUTO_RELOAD**: Boolean value to enable/disable template auto-reloading (useful for development).

---

For further information, please refer to the official [Flask documentation](https://flask.palletsprojects.com/en/2.0.x/), [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/14/), and [Flask-JWT-Extended documentation](https://flask-jwt-extended.readthedocs.io/en/stable/).
