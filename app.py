"""
    app.py
"""
import os
import subprocess
import time
from glob import glob
from datetime import datetime
from flask import make_response, jsonify, request
from app_factory import create_app
from nimble.repo import Repository
from nimble.constants import CLIENT_SEARCH_FIELDS
from db import engine as db_engine

SEED_PATH = "./db/seeds/seed_*.py"
MIGRATION_PATH = "./db/migrations/migration_*.py"

app = create_app()


@app.route("/contacts", methods=["GET"])
def search():
    """
    Search for contacts based on a search query.

    Parameters:
    - None

    Returns:
    - HTTP response with a JSON object containing the search result.

    Raises:
    - HTTP 400 Bad Request if no search query is provided.
    """
    search_query = request.args.get("search")
    if not search_query:
        return make_response(jsonify({"response": "No search query"}), 400)
    result = Repository(db_engine, "users").search(search_query, CLIENT_SEARCH_FIELDS)
    return make_response(jsonify({"response": result}), 200)


@app.route("/alive", methods=["GET"])
def alive():
    """
    Check service status
    """
    return make_response(jsonify({"response": "Alive", "date": datetime.now()}), 200)


@app.errorhandler(404)
def not_found_error(error):
    """
    Handle the 404 error and return a JSON response indicating that the resource was not found.

    Parameters:
        error (Exception): The error object representing the 404 error.

    Returns:
        response (Response): A JSON response object with a status code
        of 404 and a message indicating that the resource was not found.
    """
    print(error)
    return make_response(jsonify({"response": "Not found"}), 404)


@app.errorhandler(500)
def server_error(error):
    """
    Error handler for server errors.

    :param error: The error that occurred.
    :type error: Exception

    :return: The HTTP response with the error message.
    :rtype: Response
    """
    print(error)
    return make_response(jsonify({"response": "Internal server error"}), 500)


if __name__ == "__main__":
    seeds_path = glob(SEED_PATH)
    migrations_path = glob(MIGRATION_PATH)
    time.sleep(2)

    try:
        for migration in migrations_path:
            print("Applying migrations -> ", migration)
            subprocess.run(["python", migration], check=True)
        for seed in seeds_path:
            print("Seeding DB with -> ", seed)
            subprocess.run(["python", seed], check=True)
    except subprocess.CalledProcessError as err:
        print(err)
    app.run(host=os.environ.get("FLASK_RUN_HOST"))
