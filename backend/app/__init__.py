from flask import Flask

from .config import DevConfig
from .cli.typeform_import import import_cmd

from .api import init_api
from .extensions import init_extensions

def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.cli.add_command(import_cmd)

    init_api(app)
    init_extensions(app)

    return app