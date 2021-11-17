import json

from flask import Flask
from flask_cors import CORS

from server.model import init as init_model
from server.script import init as init_script
from server.view import init as init_view


def create_app():
    app = Flask(__name__)

    with open("settings.json") as f:
        app.config.from_mapping(
            json.load(f)
        )

    # register endpoint
    init_view(app)

    # register model
    init_model(app)

    # register script
    init_script(app)

    # CORS
    CORS(app, resources={"*": {"origins": "*"}})

    return app
