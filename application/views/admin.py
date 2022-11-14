from flask import Blueprint, render_template, request

from application.models import UserORM

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/")
def admin_index():
    return render_template("admin/index.html")


@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/console/console1.html")


@admin_bp.route("/admin/workspace_admin")
def workspace_admin():
    return render_template("admin/worksapce/space.html")


@admin_bp.route("/admin/system_user")
def system_user():
    return render_template("admin/system/user.html")


@admin_bp.route("/admin/system_user/add")
def add_user():
    return render_template("admin/system/add_user.html")


@admin_bp.route("/admin/system_user/edit")
def edit_user():
    return render_template("admin/system/edit_user.html")


# @admin_bp.route("/admin/system_user/edit/<int:user_id>")
# def edit_user(user_id):
#     user = UserORM.query.get(user_id)
#     if not user:
#         return {"status": "fail", "message": "该用户不存在或已被删除"}
#     return render_template("admin/system/edit_user.html")


@admin_bp.route("/admin/system_article")
def system_role():
    return render_template("admin/system/article.html")


@admin_bp.route("/admin/system_category")
def system_power():
    return render_template("admin/system/category.html")


@admin_bp.route("/admin/system_department")
def system_department():
    return render_template("admin/system/deptment.html")


@admin_bp.route("/admin/echarts_line")
def echarts_line():
    return render_template("admin/echarts/line.html")


@admin_bp.route("/admin/echarts_column")
def echarts_column():
    return render_template("admin/echarts/column.html")
