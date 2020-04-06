import os
import unittest

from scrapy.http import Request, Response

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
class DevTests(unittest.TestCase):
    def test_something(self):
        assert True
