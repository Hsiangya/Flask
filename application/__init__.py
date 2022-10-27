import os

from flask import Flask

from application import models
from application.common.utils import setup_log
from application.extensions import db, migrate
from application.views import auth_bp, index_bp
from configs import config


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
    """绑定插件"""
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprint(app: Flask):
    """注册蓝图"""
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
