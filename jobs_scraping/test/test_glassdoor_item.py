from jobs_scraping import JobItem
import unittest


class JobItemTests(unittest.TestCase):
    def test_all_values_are_setup_correctly(self):
        item = JobItem()
        item["position"] = "Test position"
        item["url"] = "http://testurl.com"
        item["company"] = "Some test company"
        item["location"] = "Some test location"
        item["country"] = "Some country"

        self.assertEqual(item["position"], "Test position")
        self.assertEqual(item["url"], "http://testurl.com")
        self.assertEqual(item["company"], "Some test company")
        self.assertEqual(item["location"], "Some test location")
        self.assertEqual(item["country"], "Some country")
