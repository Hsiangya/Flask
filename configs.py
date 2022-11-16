# -*- coding: utf-8 -*-
import logging
import os

from dotenv import load_dotenv

from secret_data import REDIS_HOST, REDIS_PORT, SQLALCHEMY_DATABASE_URI


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev key")

    # mysql 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI["development"]

    # redis配置
    # REDIS_HOST = REDIS_HOST
    # REDIS_PORT = REDIS_PORT
    # REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_HOST = "hsiangyatang.cn"
    REDIS_PORT = 6379
    # REDIS_PORT = os.getenv("REDIS_PORT")


class DevelopmentConfig(BaseConfig):
    """开发配置"""

    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI["development"]
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOG_LEVEL = logging.DEBUG


class TestingConfig(BaseConfig):
    """测试配置"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # 内存数据库


class ProductionConfig(BaseConfig):
    """生成环境配置"""

    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI["production"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = logging.ERROR


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

basedir = os.path.abspath(os.path.dirname(__name__))
dot_env_path = os.path.join(basedir, ".env")
flask_env_path = os.path.join(basedir, ".flaskenv")
if os.path.exists(dot_env_path):
    load_dotenv(dot_env_path)
if os.path.exists(flask_env_path):
    load_dotenv(flask_env_path)
