from flask import Flask

from server.view import init as init_view
from server.model import init as init_model


def create_app():
    app = Flask(__name__)

    # register endpoint
    init_view(app)

    # register model
    init_model(app)

    return app
