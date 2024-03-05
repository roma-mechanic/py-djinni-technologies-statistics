import scrapy
from scrapy.http import Response


class DjinniSpySpider(scrapy.Spider):
    name = "djinni_spy"
    allowed_domains = ["djinni.co"]

    # start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    def start_requests(self):
        url = "https://djinni.co/jobs/?primary_keyword=Python"
        headers = {
            "Accept-Language": "en"
        }  # Set the Accept-Language header to English
        yield scrapy.Request(url, headers=headers, callback=self.parse_posts)

    def parse_posts(self, response: Response, **kwargs):
        for job_item in response.css(".job-list__item"):
            item = {
                "title": job_item.css(".job-list-item__title > div > a::text")
                .get()
                .strip(),
                "company": job_item.css(
                    "div > header > div.d-flex.align-items-center.font-size-small.mb-2 > div > a::text"
                )
                .get()
                .strip(),
                "description": job_item.css(
                    ".job-list-item__description > span::text"
                )
                .get()
                .strip(),
                "posted_date": job_item.css(
                    "div > header > div.d-flex.align-items-center.font-size-small.mb-2 > span.job-list-item__counts.d-none.d-lg-inline-block.nobr > span > span.mr-2.nobr::attr(title)"
                )
                .get()
                .strip(),
                "views": job_item.css(
                    "div > header > div.d-flex.align-items-center.font-size-small.mb-2 > span.job-list-item__counts.d-none.d-lg-inline-block.nobr > span > span:nth-child(2) > span:nth-child(1)::attr(title)"
                )
                .get()
                .split(" ")[0],
                "applications": job_item.css(
                    "div > header > div.d-flex.align-items-center.font-size-small.mb-2 > span.job-list-item__counts.d-none.d-lg-inline-block.nobr > span > span:nth-child(2) > span:nth-child(2)::attr(title)"
                )
                .get()
                .split(" ")[0],
            }
            yield item
        next_page = response.css(
            "body > div.wrapper > div:nth-child(3) > div > div.col-lg-8.row-mobile-order-2 > main > ul.pagination.pagination_with_numbers > li:last-child > a::attr(href)"
        ).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_posts)


# https: // djinni.co / set_lang?code = en & amp;
# next = %2
# F
# "/set_lang?code=en&amp;next=%2F"
# https: // djinni.co / jobs /?primary_keyword = Python
