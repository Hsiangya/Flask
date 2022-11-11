import random

from flask import Blueprint, Flask, request
from flask.views import MethodView

from application.models import UserORM

admin_api_bp = Blueprint("admin_api", __name__, url_prefix="/api/v1/admin")


def register_api_func(app, view, endpoint, url, pk="id", pk_type="int"):
    """
    register_api_func(admin_api_bp, UserAPI, "user_api", "/user/", pk="user_id")
     :param app: flask 对象
     :param view: 视图类对象
     :param endpoint: 端点
     :param url:
     :param pk:
     :param pk_type:
     :return:
    """
    """类方法转换为视图函数"""
    view_func = view.as_view(endpoint)
    """添加url规则"""
    app.add_url_rule(
        url,
        defaults={pk: None},
        view_func=view_func,
        methods=[
            "GET",
        ],
    )
    app.add_url_rule(
        url,
        view_func=view_func,
        methods=[
            "POST",
        ],
    )
    app.add_url_rule(
        f"{url}<{pk_type}:{pk}>", view_func=view_func, methods=["GET", "PUT", "DELETE"]
    )


class UserAPI(MethodView):
    def get(self, user_id):
        if user_id is None:
            page = request.args.get("page", default=1, type=int)
            per_page = request.args.get("limit", default=10, type=int)
            filters = []
            paginate = UserORM.query.filter(*filters).paginate(
                page=page, per_page=per_page, error_out=False
            )

            return {
                "code": 0,
                "msg": "请求成功",
                "count": paginate.total,
                "data": [user.json() for user in paginate.items],
            }
        else:
            # 显示一个用户
            pass

    def post(self):
        # 创建一个新用户
        username = request.json.get("username")
        nick_name = request.json.get("nick_name") or username
        password = request.json.get("password")
        gender = request.json.get("gender", "SECRET")
        mobile = request.json.get("phone")
        email = request.json.get("email")
        avatar_url = request.json.get("avatar_url")
        birthday = request.json.get("birthday")
        signature = request.json.get("signature")

        """判断数据是否已存在"""
        """1.判断账号是否已经存在"""
        if UserORM.query.filter(UserORM.username == username).first():
            return {"status": "fail", "message": "该账号已存在"}
        """2.判断昵称是否已经被占用，若占用末尾复制随机数"""
        while UserORM.query.filter(UserORM.nick_name == nick_name).first():
            random_number = random.randint(0, 99999)
            if len(nick_name) >= 38:
                nick_name = nick_name[:29]
            nick_name = nick_name + "%06d" % random_number
        """3.判断手机号是否已存在"""
        if UserORM.query.filter(UserORM.mobile == mobile).first():
            return {"status": "fail", "message": "该手机号已存在"}

        user = UserORM()
        user.username = username
        user.nick_name = nick_name
        user.password = password
        user.gender = gender
        user.mobile = mobile
        user.email = email
        user.avatar_url = avatar_url
        user.birthday = birthday
        user.signature = signature
        user.save_to_db()
        return {"status": "success", "message": "用户添加成功"}

    def delete(self, user_id):
        user = UserORM.query.get(user_id)
        if not user:
            return {"status": "fail", "message": "该用户不存在或已被删除"}
        user.delete_from_db()
        return {"status": "success", "message": "用户删除成功"}

    def put(self, user_id):
        # update a single user
        pass


def register_api(app: Flask):
    """API注册到蓝图上"""
    register_api_func(admin_api_bp, UserAPI, "user_api", "/user/", pk="user_id")

    """注册蓝图"""
    app.register_blueprint(admin_api_bp)
