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
def register_view():
    return render_template("bbs/register.html")


@index_bp.route("/register", methods=["POST"])
def register_view2():
    """获取参数"""
    captcha_code_uuid = request.json.get("captcha_code_uuid")
    captcha_code = request.json.get("captcha_code")
    username = request.json.get("username")
    password = request.json.get("password")
    mobile = request.json.get("mobile")
    sms_captcha = request.json.get("sms_captcha")
    """校验参数"""
    real_captcha_code = redis.strict_redis.get("captcha_code_uuid_" + captcha_code_uuid)
    # 如果没有验证码或验证码不正确
    if not (real_captcha_code and real_captcha_code == captcha_code):
        return {"status": "fail", "message": "验证码错误，请输入正确的验证码"}

    return {"status": "success", "message": "注册成功，现在可以去登录了"}


@index_bp.route("/sms_code", methods=["POST"])
def sms_code():
    captcha_code = request.json.get("captcha_code")
    print(captcha_code)
    return "123"


@index_bp.route("/get_captcha")
def get_captcha():
    """获取前端生成的uuid"""
    captcha_code_uuid = request.args.get("captcha_code_uuid")
    """后端生成验证码"""
    image, code = get_captcha_image()
    """将uuid与验证码的值以键值对形式存储在redis中"""
    redis.strict_redis.setex(
        "captcha_code_uuid_" + captcha_code_uuid,
        constants.IMAGE_CODE_REDIS_EXPIRES,
        code,
    )
    """ 将图片制作成响应体返回前端"""
    response = make_response(image)
    """指定响应体格式"""
    response.content_type = "image/png"
    return response
