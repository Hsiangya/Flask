from flask import Blueprint, current_app

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def index():
    return "hello word ！"


@index_bp.route("/favicon.ico")
def favicon():
    """图标展示,无法显示 待处理"""
    return current_app.send_static_file("images/Doraemon.ico")
