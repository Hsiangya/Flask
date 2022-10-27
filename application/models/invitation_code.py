from datetime import datetime

from application.extensions import db


class InvitationCodeORM(db.Model):
    """邀请码"""

    __tablename__ = "bg_invitation_code"
    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    invite_id = db.Column(
        db.Integer, db.ForeignKey("info_user.id"), primary_key=True
    )  # 用户编号
    code = db.Column(db.String(6), nullable=False)  # 邀请码
    accept_id = db.Column(
        db.Integer, db.ForeignKey("info_user.id"), primary_key=True
    )  # 用户编号
    enable = db.Column(db.Boolean, comment="是否启用")

    create_at = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
