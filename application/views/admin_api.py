import random

from flask import Blueprint, Flask, request
from flask.views import MethodView

from application.models import ArticleORM, CategoryORM, UserORM

admin_api_bp = Blueprint("admin_api", __name__, url_prefix="/api/v1/admin")


def get_api(pk, orm):
    """主键与orm"""
    if pk is None:
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
        data = orm.query.get(pk)
        return {"code": 0, "msg": "请求成功", "data": data.json()}


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
        category = CategoryORM.query.filter(CategoryORM.id == category_id).first()
        print(category.id)
        if not category:
            return {"status": "fail", "message": "该分类不存在或已被删除"}
        category.delete_from_db()
        return {"status": "success", "message": "分类删除成功"}

    def put(self, user_id):
        # update a single user
        pass


class ArticleAPI(MethodView):
    def get(self, article_id):
        return get_api(article_id, ArticleORM)


def register_api(app: Flask):
    """API注册到蓝图上"""
    register_api_func(admin_api_bp, UserAPI, "user_api", "/user/", pk="user_id")
    register_api_func(
        admin_api_bp, CategoryAPI, "category_api", "/category/", pk="category_id"
    )
    register_api_func(
        admin_api_bp, ArticleAPI, "article_api", "/article/", pk="article_id"
    )
    """注册蓝图"""
    app.register_blueprint(admin_api_bp)
