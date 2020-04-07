from jobs_scraping import GlassdoorScrapingItem
import unittest


class GlassdoorScrapingItemTests(unittest.TestCase):
    def test_all_values_are_setup_correctly(self):
        item = GlassdoorScrapingItem()
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
