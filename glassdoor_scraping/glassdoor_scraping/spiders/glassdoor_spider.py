# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

FILENAME = "glassdoor.txt"


class GlassdoorSpider(CrawlSpider):
    name = "glassdoor_spider"

    start_urls = ["https://www.glassdoor.com/Job/python-jobs-SRCH_KO0,6.htm"]
    base_url = "https://www.glassdoor.com/"
    current_page = 1
    max_pages = 3

    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_css=".next"),
            callback="parse_page",
            follow=True,
        ),
    )

    def parse_page(self, response):
        self.current_page += 1
        if self.current_page >= self.max_pages:
            raise CloseSpider("Spider has reached maximum number of pages")
        links = response.css("a.jobLink.jobInfoItem.jobTitle::attr(href)").extract()
        for link in links:
            absolute_url = self.base_url + link[1:]
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    def parse_attr(self, response):
        with open(FILENAME, "a+") as f:
            f.write(f'{response.css("h2.mt-0.mb-xsm.strong::text").extract()}\n')
            f.write(f'{response.css(".desc::text").extract()}\n')
            f.write(
                "====================================================================================\n"
            )
