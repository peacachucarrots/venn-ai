from flask import Flask
from flask_cors import CORS

from .config import DevConfig
from .cli.typeform_import.cli import import_cmd

from .api import init_api
from .extensions import init_extensions

def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.cli.add_command(import_cmd)

    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    init_api(app)
    init_extensions(app)

    return app