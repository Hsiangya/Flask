from flask import Blueprint, current_app, render_template
from flask_login import current_user

from application.models import ArticleORM, CommentORM

article_bp = Blueprint("article", __name__)


@article_bp.route("/article/<int:article_id>")
def article_view(article_id):
    article = ArticleORM.query.get(article_id)

    """热门文章数据 返回点击前10的文章对象"""
    click_article_list = (
        ArticleORM.query.order_by(ArticleORM.clicks.desc()).limit(10).all()
    )

    """判断当前用户收藏了哪些文章"""
    is_collection = False
    if current_user.is_active:
        if article in current_user.collection_articles:
            is_collection = True

    """该文章的评论"""
    comments = []
    try:
        comments = (
            CommentORM.query.filter(CommentORM.article_id == article_id)
            .order_by(CommentORM.create_at.desc())
            .all()
        )
    except Exception as e:
        current_app.logger.error(e)
    return render_template(
        "bbs/article.html",
        is_collection=is_collection,
        click_article_list=click_article_list,
        article=article,
        comments=comments,
    )
