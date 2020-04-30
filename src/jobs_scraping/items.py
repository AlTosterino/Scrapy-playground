# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):

    """Iten for glassdoor spider."""

    position = scrapy.Field()
    link_to_job_link = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    country = scrapy.Field()
    fields_to_export = ("position", "link_to_job_link", "company", "location", "country")
