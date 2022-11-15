from flask import Blueprint, current_app, render_template

from application.common.utils import admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/")
@admin_required
def admin_index():
    return render_template("admin/index.html")


@admin_bp.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    return render_template("admin/console/console1.html")


@admin_bp.route("/admin/workspace_admin")
@admin_required
def workspace_admin():
    return render_template("admin/worksapce/space.html")


@admin_bp.route("/admin/system_user")
@admin_required
def system_user():
    return render_template("admin/system/user.html")


@admin_bp.route("/admin/system_user/add")
@admin_required
def add_user():
    return render_template("admin/system/add_user.html")


@admin_bp.route("/admin/system_user/edit")
@admin_required
def edit_user():
    return render_template("admin/system/edit_user.html")


# @admin_bp.route("/admin/system_user/edit/<int:user_id>")
# def edit_user(user_id):
#     user = UserORM.query.get(user_id)
#     if not user:
#         return {"status": "fail", "message": "该用户不存在或已被删除"}
#     return render_template("admin/system/edit_user.html")


@admin_bp.route("/admin/system_article")
@admin_required
def system_role():
    return render_template("admin/system/article.html")


@admin_bp.route("/admin/system_category")
@admin_required
def system_power():
    return render_template("admin/system/category.html")


@admin_bp.route("/admin/system_department")
@admin_required
def system_department():
    return render_template("admin/system/deptment.html")


@admin_bp.route("/admin/echarts_line")
@admin_required
def echarts_line():
    return render_template("admin/echarts/line.html")


@admin_bp.route("/admin/echarts_column")
@admin_required
def echarts_column():
    return render_template("admin/echarts/column.html")


@admin_bp.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")
