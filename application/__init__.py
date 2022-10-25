import os

from flask import Flask

from application.views import auth_bp, index_bp
from common.utils import setup_log
from configs import config
from extensions import db, migrate


def create_app(config_name=None):
    app = Flask("Flask")
    if not config_name:
        config_name = os.getenv("FLASK_CONFIG", "development")
    app.config.from_object(config[config_name])
    setup_log(config_name)
    register_extensions(app)
    register_blueprint(app)
    return app


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprint(app: Flask):
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
