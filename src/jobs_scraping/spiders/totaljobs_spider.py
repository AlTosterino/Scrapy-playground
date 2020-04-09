# -*- coding: utf-8 -*-
import w3lib.html
import scrapy
import random
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


from jobs_scraping.items import JobItem


class TotaljobsSpider(CrawlSpider):

    """
    [THIS SPIDER IS BROKEN, MAX 1 PAGE]
    Spider for extracting Python job offers from Totaljobs.
    
    So, totaljobs.com have multiple ways to ban spider from scrapping.
    Using multiple User-Agents, no User-Agents, duplicating headers with cookies
    from browser - nothing worked.

    After 2/3/5 page, there is timeout issue.
    Looking forward to scrapping from different IPs (proxies)
    
    For now this spider cannot be used with this configuration.

    However, there is a way for scraping totaljobs - do not follow
    links to every job, just scrap jobs from ?page1/?page3 etc.
    This approach eliminates way for getting full description of the job.
    
    """

    name = "totaljobs_spider"
    file_name = "Totaljobs"
    initial_country = "England"

    start_urls = ["https://www.totaljobs.com/jobs/python"]
    base_url = "https://www.totaljobs.com/"

    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_css="a.btn.btn-default.next"),
            callback="parse_page",
            follow=True,
        ),
    )

    custom_settings = {
        "ITEM_PIPELINES": {"jobs_scraping.pipelines.CSVExportPipeline": 300},
        "USER_AGENT": "",
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

        @url https://www.totaljobs.com/jobs/python

        @returns requests 19
        """
        if self.current_page > self.max_page:
            raise CloseSpider("Spider has reached maximum number of pages")
        links = response.css("div.job-title>a::attr(href)").getall()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_job)
        self.current_page += 1

    def parse_job(self, response):
        """
        Method for scraping jobs.
        
        This spider contract is broken (see class docstring)
        Url should be link to specify job, but scrapy gets timeout
        @url https://www.totaljobs.com/jobs/python

        @returns items 1

        @scrapes position company location url country
        """
        item = JobItem()
        position = response.css("h1.brand-font::text").get()
        item["position"] = position.strip() if position else position
        # Due to different elemetns keeping location, check both of them
        if temp_location := response.css(".travelTime-locationText>ul>li::text").get():
            item["location"] = temp_location
        elif temp_location := response.css("li.location>div").getall():
            item["location"] = w3lib.html.remove_tags(temp_location[0]).strip()
        else:
            item["location"] = "No location"
        item["company"] = response.css("#companyJobsLink::text").get()
        item["country"] = self.initial_country
        item["url"] = response.url
        yield item
