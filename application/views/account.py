from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from werkzeug.datastructures import FileStorage

from application.common.utils import upload_file
from application.models.user import UserORM, db

account_bp = Blueprint("account", __name__)


@account_bp.route("/account")
@account_bp.route("/account/info")
@login_required
def account_info():
    return render_template("account/index.html")


@account_bp.post("/account/info")
def account_info2():
    """获取参数"""
    current_user.username = request.json.get("username")
    current_user.signature = request.json.get("signature")
    current_user.gender = request.json.get("gender")
    current_user.birthday = request.json.get("birth_day")
    current_user.save_to_db()
    return {"status": "success", "message": "修改基本信息成功"}


@account_bp.get("/account/avatar")
def account_avatar():
    return render_template("account/user_avatar.html")


@account_bp.post("/account/avatar")
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
def account_password():
    return render_template("account/user_password.html")


@account_bp.get("/account/followed")
def account_followed():
    return render_template("account/followed.html")


@account_bp.get("/account/collection")
def account_collection():
    return render_template("account/collection.html")


@account_bp.get("/account/articles")
def account_articles():
    return render_template("account/articles.html")


@account_bp.get("/account/release")
def account_release():
    return render_template("account/release.html")
