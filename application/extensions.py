from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from application.common.redis_utils import RedisStore

db = SQLAlchemy()
migrate = Migrate()
redis = RedisStore()
