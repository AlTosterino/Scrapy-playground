# pylint: disable=no-member
# Pylint doesn't know that mutliple_crawlers.process
# is a mock object, so disable warning
import unittest

from mock import patch, call

from jobs_scraping.spiders.glassdoor_spider import GlassdoorSpider
from scrap import MultipleCrawlers


class ScrapScripTests(unittest.TestCase):
    @patch("scrap.CrawlerProcess")
    @patch("scrap.get_project_settings")
    def test_process_is_set_when_initializing(self, get_settings_mock, process_mock):
        get_settings_mock.return_value = {"TEST"}
        multiple_crawlers = MultipleCrawlers()
        process_mock.assert_called_once_with({"TEST"})
        self.assertIsNotNone(multiple_crawlers.process)

    @patch("scrap.CrawlerProcess")
    def test_can_add_one_spider(self, process_mock):
        spiders_temp = ((GlassdoorSpider, {}),)
        multiple_crawlers = MultipleCrawlers()
        multiple_crawlers.create_crawlers(spiders_temp)
        multiple_crawlers.process.crawl.assert_called_once_with(
            spiders_temp[0][0], **spiders_temp[0][1]
        )

    @patch("scrap.CrawlerProcess")
    def test_can_add_multiple_spiders(self, process_mock):
        spiders_temp = (
            (GlassdoorSpider, {}),
            (GlassdoorSpider, {"test_arg": "test"}),
        )
        multiple_crawlers = MultipleCrawlers()
        multiple_crawlers.create_crawlers(spiders_temp)
        multiple_crawlers.process.crawl.assert_has_calls(
            (
                call(spiders_temp[0][0], **spiders_temp[0][1]),
                call(spiders_temp[1][0], **spiders_temp[1][1]),
            )
        )

    @patch("scrap.CrawlerProcess")
    def test_can_start_crawling(self, process_mock):
        multiple_crawlers = MultipleCrawlers()
        multiple_crawlers.start_crawling()
        multiple_crawlers.process.start.assert_called_once()
