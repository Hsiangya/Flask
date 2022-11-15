import random

from flask import Blueprint, Flask, redirect, request
from flask.views import MethodView
from flask_login import login_user, logout_user

from application import redis
from application.common.utils import admin_required
from application.models import ArticleORM, CategoryORM, UserORM

admin_api_bp = Blueprint("admin_api", __name__, url_prefix="/api/v1/admin")


def get_api(id, orm):
    """主键与orm"""
    if id is None:
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("limit", default=10, type=int)
        filters = []
        paginate = orm.query.filter(*filters).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return {
            "code": 0,
            "msg": "请求成功",
            "count": paginate.total,
            "data": [data.json() for data in paginate.items],
        }
    else:
        """请求用户id"""
        data = orm.query.get(id)
        return {"code": 0, "msg": "请求成功", "data": data.json()}


# def delete_api(id, orm):
#     orm_object = orm.query.filter(orm.id == id).first()
#     if not orm_object:
#         return {"status": "fail", "message": "该数据不存在或已被删除"}
#     orm_object.delete_from_db()
#     return {"status": "success", "message": "删除成功"}


def register_api_func(app, view, endpoint, url, pk="id", pk_type="int"):
    """类方法转换为视图函数"""
    view_func = view.as_view(endpoint)
    """添加url规则"""
    app.add_url_rule(
        url,
        defaults={pk: None},
        view_func=view_func,
        methods=["GET"],
    )
    app.add_url_rule(
        url,
        view_func=view_func,
        methods=["POST"],
    )
    app.add_url_rule(
        f"{url}<{pk_type}:{pk}>", view_func=view_func, methods=["GET", "PUT", "DELETE"]
    )


class UserAPI(MethodView):
    def get(self, user_id):
        return get_api(user_id, UserORM)

    def post(self):
        # 创建一个新用户
        (
            avatar_url,
            birthday,
            email,
            gender,
            mobile,
            nick_name,
            password,
            signature,
            username,
        ) = self.request_info()
        """判断数据是否已存在"""
        self.query_rep(username, nick_name, mobile)
        user = UserORM()
        user.save_data(
            username,
            nick_name,
            password,
            gender,
            mobile,
            email,
            avatar_url,
            birthday,
            signature,
        )
        return {"status": "success", "message": "用户添加成功"}

    def delete(self, user_id):
        user = UserORM.query.get(user_id)
        if not user:
            return {"status": "fail", "message": "该用户不存在或已被删除"}
        user.delete_from_db()
        return {"status": "success", "message": "用户删除成功"}

    def put(self, user_id):
        # update a single user
        if not user_id:
            return {"status": "fail", "message": "该用户不存在或已被删除"}
        (
            avatar_url,
            birthday,
            email,
            gender,
            mobile,
            nick_name,
            password,
            signature,
            username,
        ) = self.request_info()

        """判断数据是否已存在"""
        self.query_rep(username, nick_name, mobile)

        user = UserORM.query.get(user_id)
        user.save_data(
            username,
            nick_name,
            password,
            gender,
            mobile,
            email,
            avatar_url,
            birthday,
            signature,
        )
        return {"status": "success", "message": "用户信息修改成功"}

    @staticmethod
    def query_rep(username, nick_name, mobile):
        """校验数据"""
        """1.判断账号是否已经存在"""
        if UserORM.query.filter(UserORM.username == username).first():
            return {"status": "fail", "message": "该账号已存在"}
        """2.判断昵称是否已经被占用，若占用末尾复制随机数"""
        if UserORM.query.filter(UserORM.nick_name == nick_name).first():
            return {"status": "fail", "message": "该昵称已存在"}
        """3.判断手机号是否已存在"""
        if UserORM.query.filter(UserORM.mobile == mobile).first():
            return {"status": "fail", "message": "该手机号已存在"}

    @staticmethod
    def request_info():
        """获取请求数据"""
        username = request.json.get("username")
        nick_name = request.json.get("nick_name", username)
        password = request.json.get("password")
        gender = request.json.get("gender", "SECRET")
        mobile = request.json.get("phone")
        email = request.json.get("email")
        avatar_url = request.json.get("avatar_url")
        birthday = request.json.get("birthday")
        signature = request.json.get("signature")
        return (
            avatar_url,
            birthday,
            email,
            gender,
            mobile,
            nick_name,
            password,
            signature,
            username,
        )


class CategoryAPI(MethodView):
    def get(self, category_id):
        return get_api(category_id, CategoryORM)

    def post(self):
        category = request.json.get("category")
        """判断数据是否已存在"""
        category_exists: CategoryORM = CategoryORM.query.get(category)
        if category_exists:
            return {"status": "fail", "message": "分类已存在"}
        category_add = CategoryORM()
        category_add.name = category
        category_add.save_to_db()
        return {"status": "success", "message": "分类添加成功"}

    def delete(self, category_id):
        category = CategoryORM.query.get(category_id)
        if not category:
            return {"status": "fail", "message": "该用户不存在或已被删除"}
        category.delete_from_db()
        return {"status": "success", "message": "用户删除成功"}

    def put(self, user_id):
        # update a single user
        pass


class ArticleAPI(MethodView):
    def get(self, article_id):
        return get_api(article_id, ArticleORM)

    def delete(self, article_id):
        article = ArticleORM.query.get(article_id)
        if not article:
            return {"status": "fail", "message": "该文章不存在或已被删除"}
        article.delete_from_db()
        return {"status": "success", "message": "文章删除成功"}


class LoginAPI(MethodView):
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")
        captcha_code_uuid = request.json.get("captcha_code_uuid")
        captcha_code = request.json.get("captcha_code")

        if not username:
            return {"status": "fail", "message": "用户名不能为空"}
        if not password:
            return {"status": "fail", "message": "密码不能为空"}
        if not captcha_code:
            return {"status": "fail", "message": "验证码不能为空"}

        real_captcha_code = redis.strict_redis.get(
            "captcha_code_uuid_" + captcha_code_uuid
        )
        if captcha_code != real_captcha_code:
            return {"status": "fail", "message": "验证码错误，请重新输入"}

        user: UserORM = UserORM.find_by_username(username)
        check_password: UserORM = UserORM.check_password(user, password=password)
        if not user:
            return {"status": "fail", "message": "该用户不存在"}
        if not check_password:
            return {"status": "fail", "message": "密码错误，请重新输入密码"}
        if not user.is_admin:
            return {"status": "fail", "message": "该用户无管理员权限"}
        login_user(user)
        return {"status": "success", "message": "登录成功，将在两秒后跳转"}


class LogoutAPI(MethodView):
    @admin_required
    def post(self):
        logout_user()
        return redirect("/")


def register_api(app: Flask):
    """API注册到蓝图上"""
    register_api_func(admin_api_bp, UserAPI, "user_api", "/user/", pk="user_id")
    register_api_func(
        admin_api_bp, CategoryAPI, "category_api", "/category/", pk="category_id"
    )
    register_api_func(
        admin_api_bp, ArticleAPI, "article_api", "/article/", pk="article_id"
    )
    """添加url规则"""
    admin_api_bp.add_url_rule("/login", view_func=LoginAPI.as_view("login_api"))
    admin_api_bp.add_url_rule("/logout", view_func=LogoutAPI.as_view("logout_api"))

    """注册蓝图"""
    app.register_blueprint(admin_api_bp)
