import json

from flask import Flask

from server.view import init as init_view
from server.model import init as init_model


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

    return app
