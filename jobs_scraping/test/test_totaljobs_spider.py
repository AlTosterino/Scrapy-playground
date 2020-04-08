import unittest
from mock import Mock

from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from jobs_scraping.spiders.totaljobs_spider import TotaljobsSpider


class TotaljobsSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = TotaljobsSpider()

    def test_file_name_is_initialized(self):
        spider = TotaljobsSpider()
        self.assertIsNotNone(spider.file_name)
        self.assertEqual(spider.file_name, "Totaljobs")

    def test_file_name_can_be_initialized(self):
        spider = TotaljobsSpider(file_name="Test name")
        self.assertIsNotNone(spider.file_name)
        self.assertEqual(spider.file_name, "Test name")

    def test_start_page_is_1(self):
        self.assertEqual(self.spider.current_page, 1)

    def test_start_page_can_be_initialized(self):
        spider = TotaljobsSpider(start_page=2)
        self.assertEqual(spider.current_page, 2)

    def test_stop_page_is_1(self):
        self.assertEqual(self.spider.max_page, 1)

    def test_stop_page_can_be_initialized(self):
        spider = TotaljobsSpider(stop_page=2)
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
            _ = [*self.spider.parse_item(response_mock)]
        response_mock.css().getall.assert_not_called()

    def test_parse_start_url_returns_parse_page(self):
        response_mock = Mock(spec=Response)
        response_mock.css().getall.return_value = ("Test Value",)
        response_mock.xpath().getall.return_value = ("Test Value",)
        data = [*self.spider.parse_start_url(response_mock)]
        self.assertIsNotNone(data)
        # I don't know if these test are good :/
        spider_mock = Mock(spec=TotaljobsSpider)
        spider_mock.parse_start_url.return_value = spider_mock.parse_item(response_mock)
        spider_mock.parse_start_url(response_mock)
        spider_mock.parse_start_url.assert_called_once_with(response_mock)
        spider_mock.parse_item.assert_called_once_with(response_mock)

    def test_spider_parse_job_yields_correct_item(self):
        response_mock = Mock(spec=Response)
        response_mock.css().getall.return_value = ("Test Value",)
        response_mock.xpath().getall.return_value = (
            '<span>\n  <a href="/jobs/in-nottingham">Nottingham</a>, <a href="/jobs/in-nottinghamshire">Nottinghamshire</a>\n</span>',
        )
        item = [*self.spider.parse_item(response_mock)][0]
        self.assertEqual(item["company"], "Test Value")
        self.assertEqual(item["location"], "Nottingham, Nottinghamshire")
        self.assertEqual(item["position"], "Test Value")
        self.assertEqual(item["url"], "Test Value")
        self.assertEqual(item["country"], "London")
