# -*- coding: utf-8 -*-
import scrapy

FILENAME = "book_titles.txt"


class FirstSpiderSpider(scrapy.Spider):
    name = "book_spider"

    def start_requests(self):
        urls = []
        for i in range(1, 20):
            urls.append(f"http://books.toscrape.com/catalogue/page-{i}.html")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        book_titles = response.css(
            "article.product_pod > h3 > a::attr(title)"
        ).extract()
        with open(FILENAME, "a+") as f:
            for title in book_titles:
                f.write(f"{title}\n")
