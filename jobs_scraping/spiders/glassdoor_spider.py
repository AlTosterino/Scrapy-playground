# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from jobs_scraping import GlassdoorScrapingItem


class GlassdoorSpider(CrawlSpider):
    """Spider for extracting Python job offers from Glassdoor"""

    name = "glassdoor_spider"
    file_name = "Glassdoor"

    start_urls = ["https://www.glassdoor.com/Job/python-jobs-SRCH_KO0,6.htm"]
    base_url = "https://www.glassdoor.com/"
    max_page = 1

    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_css=".next"),
            callback="parse_page",
            follow=True,
        ),
    )

    custom_settings = {
        "ITEM_PIPELINES": {"jobs_scraping.pipelines.GlassdoorScrapingPipeline": 300},
    }

    def __init__(self, *args, **kwargs):
        self.current_page = kwargs.get("start_page", 1)
        self.max_page = kwargs.get("stop_page", 1)
        super().__init__(*args, **kwargs)

    def parse_page(self, response):
        """Method for gathering job links

        @url https://www.glassdoor.com/Job/python-jobs-SRCH_KO0,6.htm

        @returns requests 60
        """
        if self.current_page > self.max_page:
            raise CloseSpider("Spider has reached maximum number of pages")
        self.current_page += 1
        links = response.css("a.jobLink.jobInfoItem.jobTitle::attr(href)").getall()
        for link in links:
            absolute_url = self.base_url + link[1:]
            yield scrapy.Request(absolute_url, callback=self.parse_job)

    def parse_job(self, response):
        """Method for gathering specific job information
        
        @url https://www.glassdoor.com/job-listing/fullstack-python-engineer-streetshares-JV_IC1130404_KO0,25_KE26,38.htm?jl=3147380862&ctt=1586168334926

        @returns items 1 4

        @scrapes position company location url
        """
        item = GlassdoorScrapingItem()
        item["position"] = response.css("h2.mt-0.mb-xsm.strong::text").getall()
        item["company"] = response.css("span.strong.ib::text").get()
        item["location"] = response.css("span.subtle.ib::text").getall()[1]
        item["url"] = response.url
        yield item
