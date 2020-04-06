# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from glassdoor_scraping import GlassdoorScrapingItem


class GlassdoorSpider(CrawlSpider):
    """Spider for extracting Python job offers from Glassdoor"""

    name = "glassdoor_spider"

    start_urls = ["https://www.glassdoor.com/Job/python-jobs-SRCH_KO0,6.htm"]
    base_url = "https://www.glassdoor.com/"
    current_page = 1
    max_pages = 10

    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_css=".next"),
            callback="parse_page",
            follow=True,
        ),
    )

    custom_settings = {
        "ITEM_PIPELINES": {
            "glassdoor_scraping.pipelines.GlassdoorScrapingPipeline": 300
        }
    }

    def parse_page(self, response):
        if self.current_page >= self.max_pages:
            raise CloseSpider("Spider has reached maximum number of pages")
        self.current_page += 1
        links = response.css("a.jobLink.jobInfoItem.jobTitle::attr(href)").getall()
        for link in links:
            absolute_url = self.base_url + link[1:]
            yield scrapy.Request(absolute_url, callback=self.parse_job)

    def parse_job(self, response):
        """Method for parsing job offer"""
        item = GlassdoorScrapingItem()
        item["position"] = response.css("h2.mt-0.mb-xsm.strong::text").getall()
        item["company"] = response.css("span.strong.ib::text").get()
        item["location"] = response.css("span.subtle.ib::text").getall()[1]
        item["url"] = response.url
        yield item
