class Craw:
    css_title = ".busBox3>div>div>h3>a::text"
    css_image = ".busBox3>div>.mr10>a>img::attr(src)"
    css_url = ".busBox3>div>div>h3>a::attr(href)"
    css_digest = ".busBox3>div>div:nth-child(2)>p::text"
