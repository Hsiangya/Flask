from datetime import datetime

from application.extensions import db

"""用户关注与被关注关系表"""
user_follows_table = db.Table(
    "info_user_fans",
    db.Column(
        "follower_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True
    ),  # 粉丝id
    db.Column(
        "followed_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True
    ),  # 被关注人的id
)

"""用户与文章收藏关系表"""
user_collection_table = db.Table(
    "info_user_collection",
    db.Column(
        "user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True
    ),  # 用户id
    db.Column(
        "article_id", db.Integer, db.ForeignKey("info_article.id"), primary_key=True
    ),  # 文章id
    db.Column("create_time", db.DateTime, default=datetime.now),  # 收藏创建时间
)
