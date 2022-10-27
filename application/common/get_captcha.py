# filename: qingdeng/com/get_captcha.py
from io import BytesIO
from random import choices

from captcha.image import ImageCaptcha
from PIL import Image


def gen_captcha(content="0123456789"):
    """生成验证码和图片"""
    image = ImageCaptcha()
    # 获取字符串
    captcha_text = "".join(choices(content, k=4))
    # 生成图像
    captcha_image = Image.open(image.generate(captcha_text))
    return captcha_text, captcha_image


# 生成验证码
def get_captcha_image():
    code, image = gen_captcha()
    # 图片二进制形式存入redis
    out = BytesIO()
    # session["code"] = code
    image.save(out, "png")
    out.seek(0)
    content = out.read()  # 读取图片的二进制数据做成响应体
    return content, code
