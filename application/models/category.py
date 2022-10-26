from application import db


class CategoryORM(db.Model):
    """文章分类"""

    __tablename__ = "info_category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    articles = db.relationship("ArticleORM", backref="category", lazy="dynamic")
