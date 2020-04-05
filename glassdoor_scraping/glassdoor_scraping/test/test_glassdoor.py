from scrapy.http import Response, Request
import unittest
import os

os.environ.setdefault("PRODUCTION_TESTS", "False")


@unittest.skipIf(os.environ.get("PRODUCTION_TESTS"), "Skipping development tests")
class DevTests(unittest.TestCase):
    def test_something(self):
        assert True
