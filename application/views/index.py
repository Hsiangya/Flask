import random

from flask import Blueprint, current_app, make_response, render_template, request

from application.common import constants
from application.common.get_captcha import get_captcha_image
from application.common.sms import send_sms
from application.extensions import db, redis
from application.models import UserORM

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
    phone = request.json.get("phone")
    print(type(phone))
    sms_captcha = request.json.get("sms_captcha")

    """校验图片验证码"""
    real_captcha_code = redis.strict_redis.get("captcha_code_uuid_" + captcha_code_uuid)
    print("real_captcha_code" + real_captcha_code)
    if not real_captcha_code:
        return {"status": "fail", "message": "图片验证码已过期，请重新获"}
    if real_captcha_code != captcha_code:
        return {"status": "fail", "message": "图片验证码错误，请输入正确的验证码"}

    """校验短信验证码"""
    real_sms_code = redis.strict_redis.get("sms_code" + phone)
    if not real_sms_code:
        return {"status": "fail", "message": "短信验证码已过期，请重新获"}
    if real_sms_code != sms_captcha:
        return {"status": "fail", "message": "短信验证码错误，请输入正确的验证码"}
    user = UserORM()
    user.username = username
    user.password = password
    user.mobile = phone
    db.session.add(user)
    db.session.commit()
    return {"status": "success", "message": "注册成功，现在可以去登录了"}


@index_bp.route("/sms_code", methods=["POST"])
def sms_code():
    """获取数据"""
    captcha_code = request.json.get("captcha_code")
    captcha_code_uuid = request.json.get("captcha_code_uuid")
    phone = request.json.get("phone")
    """ 校验验证码"""
    real_captcha_code = redis.strict_redis.get("captcha_code_uuid_" + captcha_code_uuid)
    # 如果没有验证码或验证码不正确
    if not real_captcha_code:
        return {"status": "fail", "message": "验证码已过期"}
    if real_captcha_code != captcha_code:
        return {"status": "fail", "message": "验证码错误，请输入正确的验证码"}

    """发送短信验证码"""
    send_sms_code = random.randint(0, 999999)
    send_sms_code = "%06d" % send_sms_code
    """redis 记录手机验证码"""
    ret = send_sms([phone], send_sms_code, "5")
    if not ret:
        current_app.logger.debug(f"短信发送失败:{phone} {send_sms_code}")
        return {"status": "fail", "message": "短信验证码发送失败"}
    else:
        current_app.logger.debug(f"短信发送成功:{phone} {send_sms_code}")
    redis.strict_redis.setex(
        "sms_code" + phone, constants.SMS_CODE_REDIS_EXPIRES, send_sms_code
    )
    return {"status": "success", "message": "短信验证码已发送，请在5分钟内完成注册"}


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


@index_bp.route("/login")
def login_view():
    return render_template("bbs/login.html")


@index_bp.route("/login", methods=["POST"])
def login_view2():
    """获取参数"""
    username = request.json.get("username")
    password = request.json.get("password")
    captcha_code_uuid = request.json.get("captcha_code_uuid")
    captcha_code = request.json.get("captcha_code")
    """校验参数"""
    real_captcha_code = redis.strict_redis.get("captcha_code_uuid_" + captcha_code_uuid)
    return {"status": "fail", "message": "登陆失败"}
