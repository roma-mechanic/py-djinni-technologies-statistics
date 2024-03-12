import scrapy
from scrapy.http import Response


class DjinniSpySpider(scrapy.Spider):
    name = "djinni_spy"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    def parse(self, response: Response, **kwargs):
        page_num = int(
            response.css(
                "body > div.wrapper > div:nth-child(3) "
                "> div > div.col-lg-8.row-mobile-order-2 "
                "> main > ul.pagination.pagination_with_numbers "
                "> li:nth-last-child(2) > a::text"
            )
            .get()
            .strip()
        )
        for page in range(1, page_num + 1):
            yield scrapy.Request(
                f"https://djinni.co/jobs/?primary_keyword=Python&page={page}",
                callback=self.parse_posts,
            )

    def parse_posts(self, response: Response):
        for job_item in response.css(".job-list__item"):
            job_info = job_item.css(".job-list-item__job-info.font-weight-500")
            nobr_texts = job_info.css("span.nobr::text").getall()
            experience_text = [
                text
                for text in nobr_texts
                if ("досвіду" or "experience") in text
            ][0][0]
            item = {
                "title": job_item.css(".job-list-item__title > div > a::text")
                .get()
                .strip(),
                "company": job_item.css(
                    "div > header > div.d-flex.align-items-center.font-size-small.mb-2 > div > a::text"
                )
                .get()
                .strip(),
                "experience": str(experience_text).strip(),
                "description": job_item.css(
                    ".job-list-item__description > span::attr(data-original-text)"
                )
                .get()
                .strip(),
                "posted_date": job_item.css(
                    "div > header > div.d-flex.align-items-center.font-size-small.mb-2 "
                    "> span.job-list-item__counts.d-none.d-lg-inline-block.nobr > span "
                    "> span.mr-2.nobr::attr(title)"
                )
                .get()
                .strip(),
                "views": job_item.css(
                    "div > header > div.d-flex.align-items-center.font-size-small.mb-2"
                    " > span.job-list-item__counts.d-none.d-lg-inline-block.nobr > span"
                    " > span:nth-child(2) > span:nth-child(1)::attr(title)"
                )
                .get()
                .split(" ")[0],
                "applications": job_item.css(
                    "div > header > div.d-flex.align-items-center.font-size-small.mb-2 "
                    "> span.job-list-item__counts.d-none.d-lg-inline-block.nobr > span "
                    "> span:nth-child(2) > span:nth-child(2)::attr(title)"
                )
                .get()
                .split(" ")[0],
            }
            yield item
