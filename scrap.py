from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from jobs_scraping.spiders.glassdoor_spider import GlassdoorSpider

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(
    GlassdoorSpider,
    start_urls=["https://www.glassdoor.com/Job/python-jobs-SRCH_KO0,6.htm"],
)
process.crawl(
    GlassdoorSpider,
    start_urls=["https://www.glassdoor.com/Job/react-jobs-SRCH_KO0,5.htm"],
)
process.start()
