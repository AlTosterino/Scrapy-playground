import unittest
from mock import Mock, MagicMock, patch, mock_open
from datetime import datetime

from jobs_scraping.pipelines import CSVExportPipeline
from jobs_scraping.items import GlassdoorScrapingItem
from jobs_scraping.spiders.glassdoor_spider import GlassdoorSpider

DATE_TIME = datetime(2020, 1, 1, 0, 0, 0)


class CSVExportPipelineTests(unittest.TestCase):
    def setUp(self):
        self.csvpipeline = CSVExportPipeline()

    @patch("jobs_scraping.pipelines.datetime")
    def test_datetime_is_set_correctly(self, mock_datetime):
        mock_datetime.now.return_value = DATE_TIME
        csvpipeline = CSVExportPipeline()
        self.assertEqual(csvpipeline.file_name, DATE_TIME.strftime("%m-%d-%Y %H-%M-%S"))

    def test_file_is_none_when_spider_was_not_opened(self):
        self.assertIsNone(self.csvpipeline.file)

    @patch("jobs_scraping.pipelines.CsvItemExporter")
    def test_export_item_is_called_with_correct_item(self, exporter_mock):
        process_item_mock = Mock(side_effect=self.csvpipeline.process_item)
        self.csvpipeline.exporter = exporter_mock
        item_mock = MagicMock(spec=GlassdoorScrapingItem)
        spider_mock = Mock(spec=GlassdoorSpider)
        process_item_mock(item_mock, spider_mock)
        process_item_mock.assert_called_once_with(item_mock, spider_mock)
        exporter_mock.export_item.assert_called_once_with(item_mock)

    @patch("jobs_scraping.pipelines.CsvItemExporter", autospec=True)
    @patch("jobs_scraping.pipelines.datetime")
    def test_open_spider_create_a_new_csv_file_and_starts_exporting(
        self, datetime_mock, exporter_mock
    ):
        datetime_mock.now.return_value = DATE_TIME
        csvpipeline = CSVExportPipeline()
        spider_mock = Mock(spec=GlassdoorSpider)
        spider_mock.file_name = "glassdoor_spider"
        with patch("builtins.open", mock_open()) as mock_file:
            csvpipeline.open_spider(spider_mock)
            generated_file_name = (
                f'{spider_mock.file_name} {DATE_TIME.strftime("%m-%d-%Y %H-%M-%S")}.csv'
            )
            mock_file.assert_called_once_with(generated_file_name, "wb")
            self.assertEqual(
                csvpipeline.file_name, generated_file_name,
            )
            exporter_mock.assert_called_once()
            self.assertEqual(
                csvpipeline.exporter.fields_to_export,
                GlassdoorScrapingItem.fields_to_export,
            )
            csvpipeline.exporter.start_exporting.assert_called_once()

    @patch("jobs_scraping.pipelines.os")
    @patch("jobs_scraping.pipelines.CsvItemExporter")
    @patch("jobs_scraping.pipelines.datetime")
    def test_close_spider_closes_file_and_finish_exporting(
        self, datetime_mock, exporter_mock, os_mock
    ):
        datetime_mock.now.return_value = DATE_TIME
        os_mock.path.getsize.return_value = 1
        csvpipeline = CSVExportPipeline()
        spider_mock = Mock(spec=GlassdoorSpider)
        spider_mock.file_name = "glassdoor_spider"
        csvpipeline.exporter = exporter_mock
        csvpipeline.file_name = (
            f'{spider_mock.file_name} {DATE_TIME.strftime("%m-%d-%Y %H-%M-%S")}.csv'
        )
        os_mock.path.realpath.return_value = csvpipeline.file_name
        mock_file = MagicMock()
        with patch("builtins.open", return_value=mock_file, create=True):
            csvpipeline.file = open(csvpipeline.file_name, "wb")
            mock_file.name = csvpipeline.file_name
            close_spider_mock = Mock(side_effect=csvpipeline.close_spider)
            close_spider_mock(spider_mock)
            os_mock.path.realpath.assert_called_once_with(csvpipeline.file_name)
            csvpipeline.exporter.finish_exporting.assert_called_once_with()
            mock_file.close.assert_called_once()
            os_mock.path.getsize.assert_called_once_with(csvpipeline.file_name)
            os_mock.remove.assert_not_called()

    @patch("jobs_scraping.pipelines.os")
    @patch("jobs_scraping.pipelines.CsvItemExporter")
    @patch("jobs_scraping.pipelines.datetime")
    def test_close_spider_removes_file_with_no_data(
        self, datetime_mock, exporter_mock, os_mock
    ):
        datetime_mock.now.return_value = DATE_TIME
        os_mock.path.getsize.return_value = 0
        csvpipeline = CSVExportPipeline()
        spider_mock = Mock(spec=GlassdoorSpider)
        spider_mock.file_name = "glassdoor_spider"
        csvpipeline.exporter = exporter_mock
        csvpipeline.file_name = (
            f'{spider_mock.file_name} {DATE_TIME.strftime("%m-%d-%Y %H-%M-%S")}.csv'
        )
        os_mock.path.realpath.return_value = csvpipeline.file_name
        mock_file = MagicMock()
        with patch("builtins.open", return_value=mock_file, create=True):
            csvpipeline.file = open(csvpipeline.file_name, "wb")
            mock_file.name = csvpipeline.file_name
            close_spider_mock = Mock(side_effect=csvpipeline.close_spider)
            close_spider_mock(spider_mock)
            os_mock.path.getsize.assert_called_once_with(csvpipeline.file_name)
            os_mock.remove.assert_called_once_with(csvpipeline.file_name)
