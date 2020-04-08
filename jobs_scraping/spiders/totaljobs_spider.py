# -*- coding: utf-8 -*-
import w3lib.html
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from jobs_scraping.items import JobItem


class TotaljobsSpider(CrawlSpider):

    """Spider for extracting Python job offers from Totaljobs."""

    name = "totaljobs_spider"
    file_name = "Totaljobs"
    initial_country = "London"

    start_urls = ["https://www.totaljobs.com/jobs/python"]
    base_url = "https://www.totaljobs.com/"

    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_css="a.btn.btn-default.next"),
            callback="parse_item",
            follow=True,
        ),
    )

    custom_settings = {
        "ITEM_PIPELINES": {"jobs_scraping.pipelines.CSVExportPipeline": 300},
        "USER_AGENT": "",
    }

    def __init__(self, *args, **kwargs):
        """Setting up current page and max page."""
        self.current_page = kwargs.get("start_page", 1)
        self.max_page = kwargs.get("stop_page", 1)
        super().__init__(*args, **kwargs)

    def parse_start_url(self, response):
        """Method for correctly scrapping first page from website."""
        return self.parse_item(response)

    def parse_item(self, response):
        """
        Method for scraping jobs.

        @url https://www.totaljobs.com/jobs/python

        @returns items 1

        @scrapes position company location url country
        """
        if self.current_page > self.max_page:
            raise CloseSpider("Spider has reached maximum number of pages")
        positions = response.css("div.job-title>a>h2::text").getall()
        locations = response.xpath(
            "/html/body/div/div/div/div/div/div/div/div/div/div/div/div/ul/li/span[span or a]"
        ).getall()
        locations = [w3lib.html.remove_tags(content).strip() for content in locations]
        companies = response.css("li.company>h3>a::text").getall()
        urls = response.css("div.job-title>a::attr(href)").getall()

        for job in zip(positions, companies, locations, urls):
            item = JobItem()
            position, company, location, url = job
            item["position"] = position
            item["company"] = company
            item["location"] = location
            item["url"] = url
            item["country"] = self.initial_country
            yield item
        self.current_page += 1
