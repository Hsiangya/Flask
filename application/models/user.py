from datetime import datetime

from flask_login import UserMixin

from application.extensions import db


class UserORM(db.Model, UserMixin):
    __tablename__ = "info_user"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    username = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    email = db.Column(db.String(50))  # 用户邮箱
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    birthday = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)  # 是否管理员
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(db.Enum("MAN", "WOMAN", "SECRET"), default="MAN")  # 男  # 女

    create_at = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # 记录的更新时间
    is_delete = db.Column(db.Boolean, default=False)
