import os

from flask import Flask

from application.common.get_bilingual import get_news
from application.common.get_life import get_life_news
from application.common.utils import setup_log
from application.extensions import db, login_manager, migrate, redis
from application.models import ArticleORM, UserORM
from application.views import article_bp, index_bp
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
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return UserORM.query.get(user_id)

    # 注册未登录跳转的页面
    login_manager.login_view = "index.login_view"


def register_blueprint(app: Flask):
    """注册蓝图"""
    app.register_blueprint(index_bp)
    app.register_blueprint(article_bp)


def register_cli(app):
    @app.cli.command()
    def create():
        """create database tables from models"""
        # db.drop_all()
        db.create_all()

    @app.cli.command()
    def get_bilingual():
        news_data = get_news(page=20)
        for article in news_data:
            Article = ArticleORM()
            try:
                (
                    Article.title,
                    Article.digest,
                    Article.index_image_url,
                    Article.content,
                    Article.create_at,
                    Article.source,
                    Article.category_id,
                    Article.user_id,
                ) = article
                Article.save_to_db()
            except Exception as e:
                print("添加失败")

    @app.cli.command()
    def get_life():
        life_data = get_life_news(page=14)
        for life in life_data:
            life_article = ArticleORM()
            try:
                (
                    life_article.title,
                    life_article.digest,
                    life_article.index_image_url,
                    life_article.content,
                    life_article.create_at,
                    life_article.source,
                    life_article.category_id,
                    life_article.user_id,
                ) = life
                life_article.save_to_db()
            except Exception as e:
                print("添加失败")
