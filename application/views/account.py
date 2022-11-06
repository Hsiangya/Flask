from flask import Blueprint, render_template
from flask_login import login_required

account_bp = Blueprint("account", __name__)


@account_bp.route("/account")
@account_bp.route("/account/info")
@login_required
def account_info():
    return render_template("account/index.html")
