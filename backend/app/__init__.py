from flask import Flask

from .api import init_api
from .config import DevConfig
from .extensions import init_extensions

def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    init_api(app)
    init_extensions(app)

    return app