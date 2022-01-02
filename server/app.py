import json

from flask import Flask
from flask_cors import CORS

from server.login import init as init_login
from server.model import init as init_model
from server.script import init as init_script
from server.view import init as init_view


def create_app():
    app = Flask(__name__)

    with open("settings.json") as f:
        app.config.from_mapping(
            json.load(f)
        )
    app.secret_key = app.config['SESSION_SECRET_KEY']

    # register endpoint
    init_view(app)

    # register model
    init_model(app)

    # register script
    init_script(app)
    
    # support login
    init_login(app)

    # CORS
    CORS(app, resources={"/api/graphql": {"origins": "*"}})

    return app
