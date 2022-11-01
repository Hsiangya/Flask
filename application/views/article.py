from flask import Blueprint, render_template

from application.models import ArticleORM

article_bp = Blueprint("article", __name__)


@article_bp.route("/article/<int:article_id>")
def article_view(article_id):
    article = ArticleORM.query.get(article_id)
    """热门文章数据 返回点击前10的文章对象"""
    click_article_list = (
        ArticleORM.query.order_by(ArticleORM.clicks.desc()).limit(10).all()
    )
    return render_template(
        "bbs/article.html", click_article_list=click_article_list, article=article
    )
