import scrapy
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from picture_spider.items import ZhaiNanSpiderItem


class ZhaiNanSpider(scrapy.Spider):
    name = "zhainan"
    allowed_domains = ['zhainanfu.com']
    start_urls = ['https://www.zhainanfu.com/tuku']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        page_count_url = hxs.xpath("//div[@class='pagination']//a[@title='末页']/@href").extract_first().strip()
        page_count = int(page_count_url.split("/")[-1])
        # print("-------------------------:", page_count)
        for i in range(1, page_count+1):
            page_url = "https://www.zhainanfu.com/tuku/page/%d" % i
            yield Request(url=page_url, callback=self.page_detail)

    def page_detail(self, response):
        # print(response.body.decode("utf-8"))
        hxs = HtmlXPathSelector(response)
        article = hxs.xpath("//div[@id='main-wrap-left']//article//h3//a")
        article_urls = article.xpath("@href").extract()
        # article_titles = article.xpath("@title").extract()
        for article_url in article_urls:
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>", article_url)
            yield Request(url=article_url, callback=self.down_pic)

    def down_pic(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.xpath("//head//title/text()").extract_first().strip()
        imgs = hxs.xpath("//div[@id='main-wrap-left']//div[@class='content']//div[@class='single-text']//img")
        # print("----------------title-------------:", title)
        for img in imgs:
            img_src = img.xpath("@src").extract_first().strip()
            # img_name = img.xpath("@alt").extract_first().strip()
            item_obj = ZhaiNanSpiderItem()
            item_obj['title'] = title
            # item_obj['name'] = img_name
            item_obj['src'] = img_src
            # print(img_name, "--->", img_src)
            yield item_obj
