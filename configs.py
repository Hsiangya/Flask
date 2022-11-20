# -*- coding: utf-8 -*-
import logging
import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
dot_env_path = os.path.join(basedir, ".env")
flask_env_path = os.path.join(basedir, ".flaskenv")
if os.path.exists(dot_env_path):
    load_dotenv(dot_env_path)
if os.path.exists(flask_env_path):
    load_dotenv(flask_env_path)


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev key")

    # mysql 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "SQLALCHEMY_DATABASE_URI_DEV"
    )
    REDIS_HOST = os.getenv("REDIS_HOST_DEV")
    REDIS_PORT = os.getenv("REDIS_PORT_DEV")


class DevelopmentConfig(BaseConfig):
    """开发配置"""

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_DEV")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOG_LEVEL = logging.DEBUG


class TestingConfig(BaseConfig):
    """测试配置"""

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_TEST")  # 内存数据库


class ProductionConfig(BaseConfig):
    """生成环境配置"""

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_PRD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = logging.ERROR
    REDIS_HOST = os.getenv("REDIS_HOST_PRD")
    REDIS_PORT = os.getenv("REDIS_PORT_PRD")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

if __name__ == "__main__":
    ENV = config["production"]
    print(ENV.REDIS_PORT, ENV.REDIS_HOST, ENV.SQLALCHEMY_DATABASE_URI)
