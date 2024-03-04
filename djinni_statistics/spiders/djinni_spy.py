import scrapy


class DjinniSpySpider(scrapy.Spider):
    name = "djinni_spy"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    def parse(self, response):
        pass
