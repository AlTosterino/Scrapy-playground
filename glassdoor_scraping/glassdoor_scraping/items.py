# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import json
from collections import OrderedDict


class GlassdoorScrapingItem(scrapy.Item):
    """Iten for glassdoor spider"""

    job = scrapy.Field()
    description = scrapy.Field()
    fields_to_export = ("job", "description")
