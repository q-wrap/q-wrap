from flask import Flask

from .routes import register_routes
from .swagger import create_swagger


def create_app() -> Flask:
    app = Flask(__name__)

    register_routes(app)
    create_swagger(app)

    return app
