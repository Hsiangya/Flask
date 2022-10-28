from flask import Blueprint, current_app, make_response, render_template, request

from application.common import constants
from application.common.get_captcha import get_captcha_image
from application.extensions import redis

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
    captcha_code_uuid = request.args.get("captcha_code_uuid")
    image, code = get_captcha_image()
    # uuid 验证码保存到redis
    redis.strict_redis.setex(
        "captcha_code_uuid_" + captcha_code_uuid,
        constants.IMAGE_CODE_REDIS_EXPIRES,
        code,
    )
    # 图片返回前端
    response = make_response(image)  # 将图片验证码图片制作成响应体
    response.content_type = "image/png"
    return response
