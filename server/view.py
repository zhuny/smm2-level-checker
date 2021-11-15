from flask import Blueprint, Flask
from flask_graphql import GraphQLView

from server.schema import schema

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.get("ping")
def ping():
    return "pong"


bp.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


def init(app: Flask):
    app.register_blueprint(bp)
