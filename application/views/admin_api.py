from flask import Blueprint, Flask, request
from flask.views import MethodView

from application.models import UserORM

admin_api_bp = Blueprint("admin_api", __name__, url_prefix="/api/v1/admin")


def register_api_func(app, view, endpoint, url, pk="id", pk_type="int"):
    view_func = view.as_view(endpoint)
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
        pass

    def delete(self, user_id):
        # 删除一个用户
        pass

    def put(self, user_id):
        # update a single user
        pass


def register_api(app: Flask):
    """API注册到蓝图上"""
    register_api_func(admin_api_bp, UserAPI, "user_api", "/user/", pk="user_id")

    """注册蓝图"""
    app.register_blueprint(admin_api_bp)
