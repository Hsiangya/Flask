import os

from flask import Flask

from application.common.utils import setup_log
from application.extensions import db, login_manager, migrate, redis
from application.models import UserORM
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
    register_cli(app)
    return app


def register_extensions(app: Flask):
    """绑定插件"""
    db.init_app(app)
    migrate.init_app(app, db)
    redis.init_app(app)
    login_manager.init_app()

    @login_manager.user_loader
    def load_user(user_id):
        return UserORM.query.get(user_id)

    # 注册未登录跳转的页面
    login_manager.login_view = "index.login_view"


def register_blueprint(app: Flask):
    """注册蓝图"""
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)


def register_cli(app):
    @app.cli.command()
    def create():
        """create database tables from models"""
        # db.drop_all()
        db.create_all()
