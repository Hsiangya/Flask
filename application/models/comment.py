from datetime import datetime

from application import db


class CommentORM(db.Model):
    """评论"""

    __tablename__ = "info_comment"

    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    content = db.Column(db.Text, nullable=False)  # 评论内容
    like_count = db.Column(db.Integer, default=0)  # 点赞条数
    user_id = db.Column(
        db.Integer, db.ForeignKey("info_user.id"), nullable=False
    )  # 用户 id
    article_id = db.Column(
        db.Integer, db.ForeignKey("info_article.id"), nullable=False
    )  # 新闻 id

    create_at = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # 记录的更新时间

    parent_id = db.Column(db.Integer, db.ForeignKey("info_comment.id"))  # 父评论 id
    parent = db.relationship("CommentORM", remote_side=[id])  # 自关联

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class CommentLikeORM(db.Model):
    """评论点赞"""

    __tablename__ = "info_comment_like"

    comment_id = db.Column(
        "comment_id", db.Integer, db.ForeignKey("info_comment.id"), primary_key=True
    )  # 评论编号
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True
    )  # 用户编号

    create_at = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # 记录的更新时间
