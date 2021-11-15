from flask import Flask

from server.view import init as init_view


def create_app():
    app = Flask(__name__)

    # register endpoint
    init_view(app)

    return app
