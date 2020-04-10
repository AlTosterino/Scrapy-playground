import pytest
from mock import Mock

from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from jobs_scraping.spiders.workpolis_spider import WorkpolisSpider


@pytest.mark.workpolis_spider
class TestWorkpolisSpider:
    @pytest.fixture
    def spider(self):
        spider = WorkpolisSpider()
        return spider

    def test_file_name_is_initialized(self):
        spider = WorkpolisSpider()
        assert spider.file_name is not None
        assert spider.file_name == "Workpolis"

    def test_file_name_can_be_initialized(self):
        spider = WorkpolisSpider(file_name="Test name")
        assert spider.file_name is not None
        assert spider.file_name == "Test name"

    def test_start_page_is_1(self, spider):
        assert spider.current_page == 1

    def test_stop_page_is_1(self, spider):
        assert spider.max_page == 1

    def test_stop_page_can_be_initialized(self):
        spider = WorkpolisSpider(stop_page=2)
        assert spider.max_page == 2

    def test_base_url_is_substring_for_start_urls(self, spider):
        for link in spider.start_urls:
            assert spider.base_url in link
            assert link.startswith(spider.base_url)

    def test_file_name_for_spider_is_not_empty(self, spider):
        assert spider.file_name is not None

    def test_closing_spider_when_max_page_reached(self, spider):
        spider.current_page = 2
        spider.max_page = 1
        response_mock = Mock(spec=Response)
        with pytest.raises(CloseSpider):
            _ = [*spider.parse_page(response_mock)]
        response_mock.css().getall.assert_not_called()

    def test_parse_start_url_returns_parse_page(self, spider):
        response_mock = Mock(spec=Response)
        test_links = ("/test1", "/test2")
        response_mock.css().getall.return_value = test_links
        data = [*spider.parse_start_url(response_mock)]
        for link in zip(data, test_links):
            assert link[0].url == f"{spider.base_url}{link[1]}"
        # I don't know if these test are good :/
        spider_mock = Mock(spec=WorkpolisSpider)
        spider_mock.parse_start_url.return_value = spider_mock.parse_page(response_mock)
        spider_mock.parse_start_url(response_mock)
        spider_mock.parse_start_url.assert_called_once_with(response_mock)
        spider_mock.parse_page.assert_called_once_with(response_mock)

    def test_spider_parse_page_yields_correct_links(self, spider):
        response_mock = Mock(spec=Response)
        test_links = ("/test1", "/test2")
        response_mock.css().getall.return_value = test_links
        spider.parse_page(response_mock)
        for link in zip([*spider.parse_page(response_mock)], test_links):
            link[0].url == f"{spider.base_url}{link[1]}"

    def test_spider_parse_job_yields_correct_item(self, spider):
        response_mock = Mock(spec=Response)
        response_mock.css().get.return_value = "Test Value"
        response_mock.url = "http://testsite.com"
        item = [*spider.parse_job(response_mock)][0]
        assert item["company"] == "Test Value"
        assert item["location"] == "Test Value"
        assert item["position"] == "Test Value"
        assert item["url"] == "http://testsite.com"
        assert item["country"] == "USA"
