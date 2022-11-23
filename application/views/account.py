from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from werkzeug.datastructures import FileStorage

from application.common.utils import upload_file
from application.models import ArticleORM, CategoryORM, UserORM

account_bp = Blueprint("account", __name__)


@account_bp.route("/account")
@account_bp.route("/account/info")
@login_required
def account_info():
    return render_template("account/index.html")


@account_bp.post("/account/info")
@login_required
def account_info2():
    """获取参数"""
    nick_name = request.json.get("nick_name")
    if UserORM.query.filter(
        UserORM.nick_name == nick_name, UserORM.id != current_user.id
    ).first():
        return {"status": "success", "message": "昵称已经存在,请修改昵称"}
    current_user.nick_name = nick_name
    current_user.signature = request.json.get("signature")
    current_user.gender = request.json.get("gender")
    current_user.birthday = request.json.get("birth_day")
    current_user.save_to_db()
    return {"status": "success", "message": "修改基本信息成功"}


@account_bp.get("/account/avatar")
@login_required
def account_avatar():
    return render_template("account/user_avatar.html")


@account_bp.post("/account/avatar")
@login_required
def account_avatar_upload():
    """获取文件内容，文件内容为2进制"""
    file: FileStorage = request.files.get("file")
    """将文件保存并返回url"""
    avatar_url = upload_file(file)
    # print("-------------" + avatar_url)
    user: UserORM = UserORM.query.get(current_user.id)
    user.avatar_url = avatar_url
    user.save_to_db()
    return {"status": "success", "message": "图片上传成功", "avatar_url": avatar_url}


@account_bp.get("/account/password")
@login_required
def account_password():
    return render_template("account/user_password.html")


@account_bp.post("/account/password")
@login_required
def account_password2():
    """获取参数"""
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")
    sure_password = request.json.get("sure_password")
    user: UserORM = current_user
    if not user.check_password(old_password):
        return {"status": "fail", "message": "旧密码输入错误"}
    if sure_password != new_password:
        return {"status": "fail", "message": "两次新密码不一致"}
    if old_password == new_password:
        return {"status": "fail", "message": "新密码不能与旧密码一样"}
    user.password = new_password
    user.save_to_db()
    return {"status": "success", "message": "修改密码成功"}


@account_bp.get("/account/followed")
@login_required
def account_followed():
    """获取分页"""
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=6, type=int)
    paginate = current_user.followed.paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("account/followed.html", paginate=paginate)


@account_bp.get("/account/collection")
@login_required
def account_collection():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    paginate = current_user.collection_articles.paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("account/collection.html", paginate=paginate)


@account_bp.get("/account/articles")
@login_required
def account_articles():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    paginate = current_user.articles.paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("account/articles.html", paginate=paginate)


@account_bp.get("/account/release")
@login_required
def account_release():
    cate_list = CategoryORM.query.all()
    return render_template("account/release.html", cate_list=cate_list)


@account_bp.post("/account/release")
@login_required
def account_release_text():
    Article = ArticleORM()
    title = request.json.get("title")
    category_id = request.json.get("cate_id")
    digest = request.json.get("describe")
    index_image_url = request.json.get("image_url")
    content = request.json.get("content")
    Article.title = title
    Article.cate_id = category_id
    Article.digest = digest
    Article.index_image_url = index_image_url
    Article.content = content
    Article.status = 1
    Article.source = current_user.nick_name
    Article.user_id = current_user.id
    Article.save_to_db()
    return {"status": "success", "message": "文章发布成功,请等待审核", "next": "/account/articles"}


@account_bp.post("/upload/article_avatar")
def article_avatar():
    """获取文件数据"""
    file: FileStorage = request.files.get("file")
    """保存文件并返回url"""
    article_avatar_url = upload_file(file)
    return {
        "status": "success",
        "message": "图片上传成功",
        "article_avatar_url": article_avatar_url,
    }
