import os
import pprint

import parsel
import requests

"""
标题,来源,摘要,文章内容 图片路径,时间
所属分类,文章作者
"""


def requests_text(url):
    """获取网页数据"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html_text = response.text
    return html_text


def get_title(html_text):
    """获取标题 图片地址 摘要"""
    selector = parsel.Selector(html_text)
    """标题"""
    title_list = selector.css(".gy_box>.gy_box_txt>.gy_box_txt2>a::text").getall()
    # print(title_list)
    """图片"""
    image_list = selector.css(".gy_box>a>img::attr(src)").getall()
    # print(image_list)
    """内容url"""
    url_list = selector.css(".gy_box>.gy_box_txt>.gy_box_txt3>a::attr(href)").getall()
    # print(url_list)
    """摘要"""
    digest_list = selector.css(".gy_box>.gy_box_txt>.gy_box_txt3>a::text").getall()
    # print(digest_list)
    index_list = zip(url_list, title_list, digest_list, image_list)
    return index_list


def get_content(html_text):
    """获取新闻文本内容 创建时间 来源"""
    selector = parsel.Selector(html_text)
    # title = selector.css(".main>.main_title").get()
    content = selector.css(".main>#Content").get()
    create_time = selector.css(".main>.main_title>p::text").get()[-16:]
    source: str = selector.css(".main>.main_title>p::text").get()[:-16].strip()
    # print(content, create_time, source)
    return [content, create_time, source]


def get_news(page=10):
    index_url = "https://language.chinadaily.com.cn/news_bilingual/page_{}.html"
    all_data = []
    for i in range(1, page + 1):
        """构造请求网页"""
        requests_url = index_url.format(i)
        print(requests_url)
        """新闻列表html"""
        index_html = requests_text(requests_url)
        """获取标题、摘要、展示图片"""
        news_list = get_title(index_html)
        for new in news_list:
            new_data = []
            content_url = "https:" + new[0]

            """添加标题 摘要 图片地址"""
            new_data.extend(list(new[1:]))

            """添加文本内容 创建时间 来源"""
            text = requests_text(content_url)
            content = get_content(text)
            new_data.extend(content)

            """添加分类id  作者id"""
            category_id = 5
            user_id = 14
            new_data.extend([category_id, user_id])

            """添加到所有数据列表中"""
            all_data.append(new_data)
            # all_data.extend()
    # print(len(all_data))
    # pprint.pprint(all_data)
    return all_data
