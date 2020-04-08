# -*- coding: utf-8 -*-
import scrapy
import w3lib.html
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from jobs_scraping.items import JobItem


class IndeedSpider(CrawlSpider):
    """Spider for extracting Python job offers from Indeed."""

    name = "indeed_spider"
    file_name = "Indeed"
    initial_country = "USA"

    start_urls = ["https://indeed.com/q-q-Python-jobs.html"]
    base_url = "https://indeed.com/"
    rules = (
        Rule(
            LinkExtractor(
                allow=(),
                restrict_xpaths='//div[@class="pagination"]/a[.//span[contains(@class, "np") and contains(text(), "Next")]]',
            ),
            callback="parse_page",
            follow=True,
        ),
    )

    custom_settings = {
        "ITEM_PIPELINES": {"jobs_scraping.pipelines.CSVExportPipeline": 300},
    }

    def __init__(self, *args, **kwargs):
        """Setting up current page and max page."""
        self.file_name = kwargs.get("filename", self.file_name)
        self.current_page = kwargs.get("start_page", 1)
        self.max_page = kwargs.get("stop_page", 1)
        super().__init__(*args, **kwargs)

    def parse_start_url(self, response):
        """Method for correctly scrapping first page from website."""
        return self.parse_page(response)

    def parse_page(self, response):
        """
        Method for gathering job links.

        @url https://www.indeed.com/q-q-Python-jobs.html

        @returns requests 10
        """
        if self.current_page > self.max_page:
            raise CloseSpider("Spider has reached maximum number of pages")
        links = response.css("div.title>a::attr(href)").getall()
        for link in links:
            absolute_url = self.base_url + link[1:]
            yield scrapy.Request(absolute_url, callback=self.parse_job)
        self.current_page += 1

    def parse_job(self, response):
        """
        Method for gathering specific job information.

        @url https://www.indeed.com/viewjob?jk=0418af813a77588a&tk=1e5ci7cij53pa800&from=serp&vjs=3

        @returns items 1

        @scrapes position company location url country
        """
        item = JobItem()
        item["position"] = response.css(
            "div.jobsearch-JobInfoHeader-title-container>h3::text"
        ).get()
        item["company"] = w3lib.html.remove_tags(
            response.xpath(
                "//div[starts-with(@class, 'jobsearch-InlineCompanyRating')]/div[1]"
            ).get()
        ).strip()
        item["location"] = w3lib.html.remove_tags(
            response.xpath(
                "//div[starts-with(@class, 'jobsearch-InlineCompanyRating')]/div[not(@class)]"
            ).get()
        ).strip()
        item["url"] = response.url
        item["country"] = self.initial_country
        yield item
