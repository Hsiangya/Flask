import random

from flask import (
    Blueprint,
    current_app,
    make_response,
    redirect,
    render_template,
    request,
)
from flask_login import current_user, login_user, logout_user

from application.common import constants
from application.common.get_captcha import get_captcha_image
from application.common.sms import send_sms
from application.extensions import redis
from application.models import ArticleORM, CategoryORM, UserORM

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def index():
    """查询分类数据"""
    category_list = CategoryORM.query.all()

    """获取前端需要显示的文章分类数据"""
    cid = request.args.get("cid", type=int, default=1)
    """获取前端需要的当前页数"""
    print(cid)
    page = request.args.get("page", type=int, default=1)
    """获取前端需要的每页数据条数"""
    per_page = request.args.get("per_page", type=int, default=10)

    """构造查询条件列表"""
    filters = []
    if cid == 1:
        pass
    else:
        """将分类查询对象添加至列表中"""
        filters.append(ArticleORM.category_id == cid)
    print(filters)
    paginate = (
        (ArticleORM.query.order_by(ArticleORM.create_at.desc()))
        .filter(*filters)
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    """热门文章数据 返回点击前10的文章对象"""
    click_article_list = (
        ArticleORM.query.order_by(ArticleORM.clicks.desc()).limit(10).all()
    )

    return render_template(
        "bbs/index.html",
        category_list=category_list,
        paginate=paginate,
        cid=cid,
        click_article_list=click_article_list,
    )


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
    # print(type(phone))
    sms_captcha = request.json.get("sms_captcha")

    """校验图片验证码"""
    real_captcha_code = redis.strict_redis.get("captcha_code_uuid_" + captcha_code_uuid)
    # print("real_captcha_code" + real_captcha_code)
    # if not real_captcha_code:
    #     return {"status": "fail", "message": "图片验证码已过期，请重新获"}
    if real_captcha_code != captcha_code:
        return {"status": "fail", "message": "图片验证码错误，请输入正确的验证码"}

    """校验短信验证码"""
    real_sms_code = redis.strict_redis.get("sms_code" + phone)
    # if not real_sms_code:
    #     return {"status": "fail", "message": "短信验证码已过期，请重新获"}
    if real_sms_code != sms_captcha:
        return {"status": "fail", "message": "短信验证码错误，请输入正确的验证码"}
    user = UserORM()
    user.nick_name = username
    user.username = username
    user.password = password
    user.mobile = phone
    user.save_to_db()
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
    if current_user.is_active:
        return redirect("/")
    return render_template("bbs/login.html")


@index_bp.route("/login", methods=["POST"])
def login_view2():
    """获取参数"""
    username = request.json.get("username")
    password = request.json.get("password")
    captcha_code_uuid = request.json.get("captcha_code_uuid")
    captcha_code = request.json.get("captcha_code")

    """校验参数"""
    """1. 校验数据是否完整"""
    if not all(
        [
            username,
            password,
        ]
    ):
        return {"status": "fail", "message": "用户名与密码不能为空"}
    """2. 校验图片验证码"""
    real_captcha_code = redis.strict_redis.get("captcha_code_uuid_" + captcha_code_uuid)
    # if not real_captcha_code:
    #     return {"status": "fail", "message": "验证码已过期，请刷新验证码"}
    if captcha_code != real_captcha_code:
        return {"status": "fail", "message": "验证码错误，请重新输入"}

    """查询该用户是否注册"""
    # 确保查询没有出错
    try:
        user: UserORM = UserORM.query.filter(UserORM.username == username).first()
    except Exception as e:
        current_app.logger.error(e)
        return {"status": "error", "message": "查询用户出错"}
    if not user:
        return {"status": "fail", "message": "该用户未注册，请先注册"}
    """检查密码是否正确"""
    if not user.check_password(password):
        return {"status": "fail", "message": "密码错误，请输入正确的密码"}

    """登录用户"""
    login_user(user)
    return {"status": "success", "message": "登录成功,将在两秒后跳转"}


@index_bp.route("/logout")
def logout():
    logout_user()
    return redirect("/")
