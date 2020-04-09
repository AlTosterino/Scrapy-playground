from typing import Tuple

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from jobs_scraping.spiders import glassdoor_spider, indeed_spider


class MultipleCrawlers:

    """Class for starting multiple crawlers in the same process."""

    def __init__(self):
        """Setting up process."""
        self.process = CrawlerProcess(get_project_settings())

    def create_crawlers(self, spiders: Tuple[Tuple[object, dict]]) -> None:
        """
        Method for defining crawlers for process.

        Arguments:
            spiders {Tuple[Tuple[object, dict]]} -- A tuple of tuples, e.g. ((Spider, {}), (Spider2, {'key': 'value}))
        """
        for config in spiders:
            spider, keywords = config
            self.process.crawl(spider, **keywords)

    def start_crawling(self) -> None:
        """Method for starting process of scrapping."""
        self.process.start()


if __name__ == "__main__":  # pragma: no cover
    spiders = (
        (
            glassdoor_spider.GlassdoorSpider,
            {
                "start_urls": [
                    "https://www.glassdoor.com/Job/python-jobs-SRCH_KO0,6.htm"
                ],
                "file_name": "Glassdoor PYTHON",
            },
        ),
        (
            glassdoor_spider.GlassdoorSpider,
            {
                "start_urls": [
                    "https://www.glassdoor.com/Job/react-jobs-SRCH_KO0,5.htm"
                ],
                "file_name": "Glassdoor REACT",
            },
        ),
        (
            indeed_spider.IndeedSpider,
            {
                "start_urls": ["https://indeed.com/q-q-Python-jobs.html"],
                "file_name": "Totaljobs PYTHON",
            },
        ),
        (
            indeed_spider.IndeedSpider,
            {
                "start_urls": ["https://indeed.com/q-q-React-jobs.html"],
                "file_name": "Totaljobs REACT",
            },
        ),
    )
    multiple_crawlers = MultipleCrawlers()
    multiple_crawlers.create_crawlers(spiders)
    multiple_crawlers.start_crawling()
