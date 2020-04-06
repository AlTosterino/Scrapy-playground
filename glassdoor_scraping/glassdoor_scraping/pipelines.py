# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.exporters import CsvItemExporter
from glassdoor_scraping import GlassdoorScrapingItem


class GlassdoorScrapingPipeline:

    file_name = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
    file = None

    def process_item(self, item, spider):
        item["country"] = "USA"
        self.exporter.export_item(item)

    def open_spider(self, spider):
        self.file_name = f"{spider.name} {self.file_name}.csv"
        self.file = open(self.file_name, "wb")
        self.exporter = CsvItemExporter(self.file)
        self.exporter.fields_to_export = GlassdoorScrapingItem.fields_to_export
        self.exporter.start_exporting()
        pass

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
