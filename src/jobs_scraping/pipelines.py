# -*- coding: utf-8 -*-


import os

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

# Define your item pipelines here
#
from scrapy.exporters import CsvItemExporter

from jobs_scraping.items import JobItem


class CSVExportPipeline:

    """Class for exporting scrapped items to CSV file."""

    def __init__(self):
        """Setting up file and file_name based on current date and time."""
        self.file_name = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
        self.file = None
        super().__init__()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        # This return prints  to stdout, so comment have clear log
        # return item

    def open_spider(self, spider):
        self.file_name = f"{spider.file_name} {self.file_name}.csv"
        self.file = open(self.file_name, "wb")
        self.exporter = CsvItemExporter(self.file)
        self.exporter.fields_to_export = JobItem.fields_to_export
        self.exporter.start_exporting()

    def close_spider(self, spider):
        file_path = os.path.realpath(self.file.name)
        self.exporter.finish_exporting()
        self.file.close()
        # Delete file if empty (More usable for testing etc.)
        if not os.path.getsize(file_path):
            os.remove(file_path)
