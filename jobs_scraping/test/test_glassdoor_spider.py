import unittest
from mock import Mock

from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from jobs_scraping.spiders.glassdoor_spider import GlassdoorSpider

# * Use this for production setting (Cache for e.g. 2/3 days)
# "HTTPCACHE_POLICY": "scrapy.extensions.httpcache.DummyPolicy",
# "HTTPCACHE_STORAGE": "scrapy.extensions.httpcache.FilesystemCacheStorage",
# "HTTPCACHE_ENABLED": True,
# "HTTPCACHE_EXPIRATION_SECS": 0,
# "HTTPCACHE_DIR": "httpcache",
# "HTTPCACHE_IGNORE_HTTP_CODES": [404],
# "HTTPCACHE_IGNORE_MISSING": False,
# "HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS": ["no-cache", "no-store"],


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
            with self.subTest(i=link):
                self.assertTrue(self.spider.base_url in link)
                self.assertTrue(link.startswith(self.spider.base_url))

    def test_file_name_for_spider_is_not_empty(self):
        self.assertIsNotNone(self.spider.file_name)

    def test_closing_spider_when_max_page_reached(self):
        self.spider.current_page = 2
        self.spider.max_page = 1
        response_mock = Mock(spec=Response)
        with self.assertRaises(CloseSpider):
            _ = [*self.spider.parse_page(response_mock)]
        response_mock.css().getall.assert_not_called()

    def test_parse_start_url_returns_parse_page(self):
        response_mock = Mock(spec=Response)
        test_links = ("/test1", "/test2")
        response_mock.css().getall.return_value = test_links
        data = [*self.spider.parse_start_url(response_mock)]
        for link in zip(data, test_links):
            with self.subTest(i=link[1]):
                self.assertEqual(link[0].url, f"{self.spider.base_url}{link[1][1:]}")
        # I don't know if these test are good :/
        spider_mock = Mock(spec=GlassdoorSpider)
        spider_mock.parse_start_url.return_value = spider_mock.parse_page(response_mock)
        spider_mock.parse_start_url(response_mock)
        spider_mock.parse_start_url.assert_called_once_with(response_mock)
        spider_mock.parse_page.assert_called_once_with(response_mock)

    def test_spider_parse_page_yields_correct_links(self):
        response_mock = Mock(spec=Response)
        test_links = ("/test1", "/test2")
        response_mock.css().getall.return_value = test_links
        self.spider.parse_page(response_mock)
        for link in zip([*self.spider.parse_page(response_mock)], test_links):
            with self.subTest(i=link[1]):
                self.assertEqual(link[0].url, f"{self.spider.base_url}{link[1][1:]}")

    def test_spider_parse_job_yields_correct_item(self):
        response_mock = Mock(spec=Response)
        response_mock.css().get.return_value = "Test Value"
        response_mock.css().getall.return_value = ["Test Value1", "Test Value2"]
        response_mock.url = "http://testsite.com"
        item = [*self.spider.parse_job(response_mock)][0]
        self.assertEqual(item["company"], "Test Value")
        self.assertEqual(item["location"], "Test Value2")
        self.assertEqual(item["position"], "Test Value")
        self.assertEqual(item["url"], "http://testsite.com")
        self.assertEqual(item["country"], "USA")
