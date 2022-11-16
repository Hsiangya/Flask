import hashlib
import logging
import os
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler

from flask import current_app, redirect
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from configs import config


def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler(
        "logs/log", maxBytes=1024 * 1024 * 100, backupCount=10
    )
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter("%(levelname)s %(filename)s:%(lineno)d %(message)s")
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def upload_file(avatar: FileStorage):
    """对图片进行重命名，处理 并存到目录中 并返回url"""
    """构造当前项目的路径"""
    path = os.path.dirname(current_app.instance_path)
    avatar_dir = os.path.join(
        path, "static", "avatar", datetime.today().strftime("%Y-%m")
    )
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir)
    """从 FileStorage 对象里面获取文件名字"""
    filename = avatar.filename
    """名字相同 内容不同"""
    suffix = filename.split(".")[-1]

    """内容相同 名字不同"""
    content = avatar.stream.read()  # 读取图片之后 就没有内容了
    name = hashlib.md5(content).hexdigest()  # 获取 md5 的值
    file_name = ".".join([name, suffix])

    """将文件保存"""
    open(os.path.join(avatar_dir, file_name), mode="wb").write(content)
    avatar_url = "/".join(
        ["/static", "avatar", datetime.today().strftime("%Y-%m"), file_name]
    )
    return avatar_url


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not (hasattr(current_user, "is_admin") and current_user.is_admin == True):
            return redirect("/admin/login")
        ret = func(*args, **kwargs)
        return ret

    return wrapper
