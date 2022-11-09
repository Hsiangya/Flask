from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
def admin_index():
    return render_template("admin/index.html")


@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/console/console1.html")


@admin_bp.route("/admin/workspace_admin")
def workspace_admin():
    return render_template("admin/system/space.html")


@admin_bp.route("/admin/system_user")
def system_user():
    return render_template("admin/system/user.html")


@admin_bp.route("/admin/system_role")
def system_role():
    return render_template("admin/system/role.html")


@admin_bp.route("/admin/system_power")
def system_power():
    return render_template("admin/system/power.html")


@admin_bp.route("/admin/system_department")
def system_department():
    return render_template("admin/system/deptment.html")


@admin_bp.route("/admin/echarts_line")
def echarts_line():
    return render_template("admin/echarts/line.html")


@admin_bp.route("/admin/echarts_column")
def echarts_column():
    return render_template("admin/echarts/column.html")
