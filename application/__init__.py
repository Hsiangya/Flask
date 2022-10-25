import os

from flask import Flask

from configs import config
from extensions import db, migrate


def create_app(config_name=None):
    app = Flask("Flask")
    if not config_name:
        config_name = os.getenv("FLASK_CONFIG", "development")
    app.config.from_object(config[config_name])
    register_extensions(app)
    return app


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
