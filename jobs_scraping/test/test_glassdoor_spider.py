import os
import unittest
from mock import Mock

from scrapy.exceptions import CloseSpider
from scrapy.http import Request, Response
from jobs_scraping.spiders.glassdoor_spider import GlassdoorSpider


os.environ["PRODUCTION_TESTS"] = "0"

# * Use this for production setting (Cache for e.g. 2/3 days)
# "HTTPCACHE_POLICY": "scrapy.extensions.httpcache.DummyPolicy",
# "HTTPCACHE_STORAGE": "scrapy.extensions.httpcache.FilesystemCacheStorage",
# "HTTPCACHE_ENABLED": True,
# "HTTPCACHE_EXPIRATION_SECS": 0,
# "HTTPCACHE_DIR": "httpcache",
# "HTTPCACHE_IGNORE_HTTP_CODES": [404],
# "HTTPCACHE_IGNORE_MISSING": False,
# "HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS": ["no-cache", "no-store"],


@unittest.skipIf(
    bool(int(os.environ.get("PRODUCTION_TESTS"))), "Skipping development tests"
)
class GlassdoorSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = GlassdoorSpider()

    def test_start_page_is_1(self):
        self.assertEqual(self.spider.current_page, 1)

    def test_start_page_can_be_initialized(self):
        spider = GlassdoorSpider(start_page=2)
        self.assertEqual(spider.current_page, 2)

    def test_stop_page_is_1(self):
        self.assertEqual(self.spider.max_page, 1)

    def test_stop_page_can_be_initialized(self):
        spider = GlassdoorSpider(stop_page=2)
        self.assertEqual(spider.max_page, 2)

    def test_base_url_is_substring_for_start_urls(self):
        for link in self.spider.start_urls:
            self.assertTrue(self.spider.base_url in link)

    def test_file_name_for_spider_is_not_empty(self):
        self.assertIsNotNone(self.spider.file_name)

    def test_closing_spider_when_max_page_reached(self):
        spider = GlassdoorSpider()
        spider.current_page = 2
        spider.max_page = 1
        response_mock = Mock(spec=Response)
        spider.parse_page(response_mock)
        with self.assertRaises(CloseSpider):
            [*spider.parse_page(response_mock)]

    def test_spider_parse_page_yields_correct_links(self):
        spider = GlassdoorSpider()
        response_mock = Mock(spec=Response)
        test_links = ("/test1", "/test2")
        response_mock.css().getall.return_value = test_links
        spider.parse_page(response_mock)
        for link in zip([*spider.parse_page(response_mock)], test_links):
            self.assertEqual(link[0].url, f"{spider.base_url}{link[1][1:]}")
