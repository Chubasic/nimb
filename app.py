"""
    app.py
"""
import os
import subprocess
import time
from glob import glob
from datetime import datetime
from flask import make_response, jsonify
from app_factory import create_app
from nimble.api.classes.contact import Contact, contact_schema
from nimble.api.classes.response import response_fields_schema
from nimble.api.nimb import fetch
from nimble.api.classes.request_params import RequestParams

SEED_PATH = "./db/seeds/seed_*.py"
MIGRATION_PATH = "./db/migrations/migration_*.py"

app = create_app()


@app.route("/testing", methods=["GET"])
def search():
    """
    Testing N.API
    """

    params = RequestParams(
        fields=["first name", "last name", "email", "description"],
        tags=0,
        per_page=20,
        page=1,
        sort=("updated", "desc"),
        record_type="person",
        query=None,
    )
    resposne = fetch("contacts", params=params)
    resources = resposne.get("resources")
    # Check how does it serialize that fast with recursion
    res = response_fields_schema.load(resources, many=True)
    return make_response(jsonify({"response": res}), 200)


@app.route("/alive", methods=["GET"])
def alive():
    """
    Check service status
    """
    return make_response(jsonify({"response": "Alive", "date": datetime.now()}), 200)


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
