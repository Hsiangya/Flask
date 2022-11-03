from flask import Blueprint, current_app, render_template, request
from flask_login import current_user

from application.extensions import db
from application.models import ArticleORM, CommentORM, UserORM

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


@article_bp.post("/article/followed_user")
def followed_user():
    """ "检查用户是否登录"""
    if not current_user.is_active:
        return {"status": "fail", "code": 4101, "message": "用户登录之后才能进行关注"}

    """解析请求参数"""
    user_id = request.json.get("user_id")
    action = request.json.get("action")

    """校验参数"""
    author: UserORM = UserORM.query.get(user_id)
    if not author:
        return {"status": "fail", "message": "作者不存在"}
    if action == "follow":
        if author not in current_user.followed:
            current_user.followed.append(author)
        else:
            return {"status": "fail", "message": "已经关注过了,不能重复关注"}
        message = "关注用户成功"
    elif action == "unfollow":
        if author not in current_user.followed:
            return {"status": "fail", "message": "未关注该用户，无法取消关注"}
        else:
            current_user.followed.remove(author)
        message = "取消关注用户成功"
    else:
        message = "操作不存在"
    db.session.commit()
    return {"status": "success", "message": message}
