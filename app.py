"""
    app.py
"""
import os
import glob
import subprocess
import time
from datetime import datetime
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.debug = os.environ.get("FLASK_DEBUG", False)
cors = CORS(
    app, origins=[os.environ.get("CORS_ALLOWED_ORIGIN")],
    methods=['GET', 'POST'])



@app.route('/', methods=['GET'])
def search():
    """
    WIP
    """
    print(request)
    return make_response(jsonify({"response": "Hello World"}), 200)

@app.route('/alive', methods=['GET'])
def main():
    """
    Check service status
    """
    return make_response(jsonify({"response": "Alive", 'date': datetime.now()}), 200)


if __name__ == "__main__":
    SEED_PATH = "./seeds/*.py"
    script_paths = glob.glob(SEED_PATH)
    time.sleep(3)
    try:
        for script_path in script_paths:
            print("runing script ", script_path)
            subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as err:
        print(err)
    app.run()
