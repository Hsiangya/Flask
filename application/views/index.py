from flask import Blueprint, current_app, render_template, request

from application.common.get_captcha import gen_captcha

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def index():
    return render_template("bbs/index.html")


@index_bp.route("/favicon.ico")
def favicon():
    """图标展示,无法显示 待处理"""
    return current_app.send_static_file("images/Doraemon.ico")


@index_bp.route("/register")
def register():
    return render_template("bbs/register.html")


@index_bp.route("/sms_code", methods=["POST"])
def sms_code():
    captcha_code = request.json.get("captcha_code")
    print(captcha_code)
    return "123"


@index_bp.route("/get_captcha")
def get_captcha():
    """图片uuid 验证码"""
    captcha_code_uuid = request.json.get("captcha_code_uuid")
    code, image = gen_captcha()
    # 保存到redis
