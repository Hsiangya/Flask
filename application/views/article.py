from flask import Blueprint, current_app, render_template, request
from flask_login import current_user

from application.extensions import db
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


@article_bp.route("/article/article_comment", methods=["POST"])
def article_comment():
    """检查用户是否登录"""
    if not current_user.is_active:
        return {"code": 4101, "message": "登录之后才能进行评论", "status": "fail"}

    """解析请求参数"""
    article_id = request.json.get("article_id")
    content = request.json.get("comment")
    parent_id = request.json.get("parent_id")

    """添加评论"""
    comment: CommentORM = CommentORM()
    comment.user_id = current_user.id
    comment.article_id = article_id
    comment.content = content
    if parent_id:
        comment.parent_id = parent_id
    comment.save_to_db()

    """返回结果"""
    return {"message": "提交评论成功", "status": "success"}


@article_bp.route("/article/article_collect", methods=["POST"])
def article_collect():
    """检查用户是否登录"""
    if not current_user.is_active:
        return {"code": 4101, "message": "登录之后才能进行收藏", "status": "fail"}

    """获取请求参数"""
    article_id = request.json.get("article_id")
    action = request.json.get("action")

    if action not in ["collect", "cancel_collect"]:
        return {"status": "fail", "message": "请求参数错误", "code": 4102}
    article: ArticleORM = ArticleORM.query.get(int(article_id))
    if not article:
        return {"status": "fail", "message": "文章不存在"}

    """执行收藏逻辑"""

    if action == "collect":
        current_user.collection_articles.append(article)
        message = "收藏文章成功"
    elif action == "cancel_collect":
        current_user.collection_articles.remove(article)
        message = "取消收藏文章成功"
    db.session.commit()
    return {"status": "success", "code": 0, "message": message}
