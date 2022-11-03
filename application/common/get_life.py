import parsel

from application.common.get_bilingual import requests_text

"""
标题,来源,摘要,文章内容 图片路径,时间
所属分类,文章作者
"""


def get_title(html_text):
    """获取标题 图片地址 摘要"""
    selector = parsel.Selector(html_text)
    """标题"""
    title_list = selector.css(".busBox3>div>div>h3>a::text").getall()
    # print(title_list)
    """图片"""
    image_list = selector.css(".busBox3>div>.mr10>a>img::attr(src)").getall()
    # print(image_list)
    """内容url"""
    url_list = selector.css(".busBox3>div>div>h3>a::attr(href)").getall()
    # print(url_list)
    """摘要"""
    digest_list = selector.css(".busBox3>div>div:nth-child(2)>p::text").getall()
    # print(digest_list)
    index_list = zip(url_list, title_list, digest_list, image_list)
    return index_list


def get_content(html_text):
    """获取新闻文本内容 创建时间 来源"""
    selector = parsel.Selector(html_text)
    # title = selector.css(".main>.main_title").get()
    content = selector.css("#Content").get()
    create_time = selector.css(".fenx>:nth-child(2)::text").get()
    source: str = selector.css(".fenx>.xinf-le>a:last-child::text").get()
    if not source:
        source: str = selector.css(".fenx>.xinf-le::text").get().strip()[3:]
    print(create_time)
    print(source)
    return [content, create_time, source]


def get_life_news(page=3):
    index_url = (
        "https://cn.chinadaily.com.cn/wenlv/5b7628c6a310030f813cf48f/page_{}.html"
    )
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
            category_id = 6
            user_id = 24
            new_data.extend([category_id, user_id])

            """添加到所有数据列表中"""
            all_data.append(new_data)
            # all_data.extend()
    # print(len(all_data))
    # pprint.pprint(all_data)
    return all_data
