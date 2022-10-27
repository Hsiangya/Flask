from common.redis_utils import RedisStore
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
redis = RedisStore()
