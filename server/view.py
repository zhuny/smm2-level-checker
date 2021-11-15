from flask import Blueprint, Flask

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.get("ping")
def ping():
    return "pong"


def init(app: Flask):
    app.register_blueprint(bp)
