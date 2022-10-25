from flask import Blueprint

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def index():
    return "hello word ！"
