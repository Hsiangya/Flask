import os


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev key")

    # mysql 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = ""

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379


class DevelopmentConfig(BaseConfig):
    """开发配置"""

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    """测试配置"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # 内存数据库


class ProductionConfig(BaseConfig):
    """生成环境配置"""

    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
