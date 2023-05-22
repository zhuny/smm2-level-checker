import json

from flask import Flask

from server2.script import init as script_init
from server2.storage import StorageController


def create_app():
    app = Flask(__name__)

    with open("settings.json") as f:
        app.config.from_mapping(
            json.load(f)
        )
    app.secret_key = app.config['SESSION_SECRET_KEY']

    app.extensions['firestore'] = StorageController()

    # register script
    script_init(app)

    return app
