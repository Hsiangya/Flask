from flask import Blueprint, Flask
from flask.views import MethodView

admin_api = Blueprint("admin_api", __name__, url_prefix="/api/v1/admin")


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
            # 返回一个包含所有用户的列表
            pass
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
    register_api_func(admin_api, UserAPI, "user_api", "/user/", pk="user_id")
    app.register_blueprint(admin_api)
