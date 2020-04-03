# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

FILENAME = "glassdoor.txt"


class GlassdoorSpider(CrawlSpider):
    name = "glassdoor_spider"

    start_urls = ["https://www.glassdoor.com/Job/python-jobs-SRCH_KO0,6.htm"]
    base_url = "https://www.glassdoor.com/"

    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_css=".next"),
            callback="parse_page",
            follow=True,
        ),
    )

    def parse_page(self, response):
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
