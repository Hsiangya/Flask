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
@login_required
def account_info2():
    """获取参数"""
    current_user.nick_name = request.json.get("nick_name")
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
    return render_template("account/followed.html")


@account_bp.get("/account/collection")
@login_required
def account_collection():
    return render_template("account/collection.html")


@account_bp.get("/account/articles")
@login_required
def account_articles():
    return render_template("account/articles.html")


@account_bp.get("/account/release")
@login_required
def account_release():
    return render_template("account/release.html")
