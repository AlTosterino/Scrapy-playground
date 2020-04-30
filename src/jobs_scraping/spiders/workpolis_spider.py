# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from jobs_scraping.items import JobItem


class WorkpolisSpider(CrawlSpider):
    """Spider for extracting Python job offers from Glassdoor."""

    name = "workpolis_spider"
    file_name = "Workpolis"
    initial_country = "USA"

    start_urls = ["https://www.workopolis.com/jobsearch/find-jobs?ak=python"]
    base_url = "https://www.workopolis.com"

    rules = (
        Rule(
            LinkExtractor(
                allow=(), restrict_css="a.Pagination-link.Pagination-link--next"
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
        self.max_page = kwargs.get("stop_page", 1)

        self.current_page = 1
        super().__init__(*args, **kwargs)

    def parse_start_url(self, response):
        """Method for correctly scrapping first page from website."""
        return self.parse_page(response)

    def parse_page(self, response):
        """
        Method for gathering job links.

        @url https://www.workopolis.com/jobsearch/find-jobs?ak=python

        @returns requests 20
        """
        if self.current_page > self.max_page:
            raise CloseSpider("Spider has reached maximum number of pages")
        links = response.css(".JobCard-titleLink::attr(href)").getall()
        for link in links:
            absolute_url = self.base_url + link
            yield scrapy.Request(absolute_url, callback=self.parse_job)
        self.current_page += 1

    def parse_job(self, response):
        """
        Method for gathering specific job information.
        
        @url https://www.workopolis.com/jobsearch/viewjob/oy-oTUTSIxJY3CCk7w1og3e5-iDqxDO6j4_oEIRs0o_amhctJv7j-Q?ak=python&l=&isp=0

        @returns items 1

        @scrapes position company location url country
        """
        item = JobItem()
        item["position"] = response.css(".ViewJobHeader-title::text").get()
        item["company"] = response.css(".ViewJobHeader-company::text").get()
        item["location"] = response.css(".ViewJobHeader-property::text").get()
        item["link_to_job_link"] = response.url
        item["country"] = self.initial_country
        yield item
