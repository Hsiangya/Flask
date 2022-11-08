from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from application.extensions import db

from .relationship_table import user_collection_table, user_follows_table


class UserORM(db.Model, UserMixin):
    """
    id、用户昵称、密码、手机号、邮箱、头像路径、最后一次登录时间、是否管理员、用户签名、性别、创建时间、更新时间
    发布的文章------>1对多
    用户发表的评论---->一对多
    点赞的评论---->一对多
    收藏的文章------>多对多----->与关系表进行绑定
    关注的人/粉丝--->多对多 ---->自我关联
    """

    __tablename__ = "info_user"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    username = db.Column(db.String(32), unique=True, nullable=False)  # 用户账号
    nick_name = db.Column(db.String(38), unique=True)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    email = db.Column(db.String(50))  # 用户邮箱
    avatar_url = db.Column(
        db.String(256), default="/static/images/person.png"
    )  # 用户头像路径
    birthday = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)  # 是否管理员
    signature = db.Column(db.String(512), default="用户很懒，什么都没留下")  # 用户签名
    gender = db.Column(db.Enum("MAN", "WOMAN", "SECRET"), default="MAN")  # 男  # 女

    create_at = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # 记录的更新时间
    is_delete = db.Column(db.Boolean, default=False)

    """一对多关系"""
    articles = db.relationship("ArticleORM", backref="user", lazy="dynamic")  # 发布的文章
    comments = db.relationship("CommentORM", backref="user", lazy="dynamic")  # 用户发布的评论
    commit_likes = db.relationship("CommentLikeORM", backref="user")  # 用户点赞的评论

    """多对多关系"""
    collection_articles = db.relationship(
        "ArticleORM", secondary=user_collection_table, lazy="dynamic"
    )  # 收藏的文章
    followers = db.relationship(
        "UserORM",
        secondary=user_follows_table,
        primaryjoin=id == user_follows_table.c.followed_id,
        secondaryjoin=id == user_follows_table.c.follower_id,
        backref=db.backref("followed", lazy="dynamic"),
        lazy="dynamic",
    )  # 关注的用户/粉丝   自我关联

    def json(self):
        """ "获取用户数据"""
        return {
            "id": self.id,
            "username": self.username,
            "mobile": self.mobile,
            "email": self.email,
            "avatar_url": self.avatar_url,
            "birthday": self.birthday,
            "is_admin": self.is_admin,
            "signature": self.signature,
            "gender": self.gender,
            "create_at": self.create_at.strftime("%Y-%M-%d"),
            "update_at": self.update_at,
            "is_delete": self.is_delete,
        }

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
