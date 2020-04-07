from typing import Tuple

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from jobs_scraping.spiders.glassdoor_spider import GlassdoorSpider


class MultipleCrawlers:
    def __init__(self):
        self.process = CrawlerProcess(get_project_settings())

    def create_crawlers(self, spiders: Tuple[Tuple[object, dict]]) -> None:
        for config in spiders:
            spider, keywords = config
            self.process.crawl(spider, **keywords)

    def start_crawling(self) -> None:
        self.process.start()


if __name__ == "__main__":  # pragma: no cover
    spiders = (
        (
            GlassdoorSpider,
            {
                "start_urls": [
                    "https://www.glassdoor.com/Job/python-jobs-SRCH_KO0,6.htm"
                ]
            },
        ),
        (
            GlassdoorSpider,
            {"start_urls": ["https://www.glassdoor.com/Job/react-jobs-SRCH_KO0,5.htm"]},
        ),
    )
    multiple_crawlers = MultipleCrawlers()
    multiple_crawlers.create_crawlers(spiders)
    multiple_crawlers.start_crawling()
