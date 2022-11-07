from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

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
