import pytest

from jobs_scraping.items import JobItem

pytestmark = pytest.mark.job_item


def test_all_values_are_setup_correctly():
    item = JobItem()
    item["position"] = "Test position"
    item["url"] = "http://testurl.com"
    item["company"] = "Some test company"
    item["location"] = "Some test location"
    item["country"] = "Some country"

    assert item["position"] == "Test position"
    assert item["url"] == "http://testurl.com"
    assert item["company"] == "Some test company"
    assert item["location"] == "Some test location"
    assert item["country"] == "Some country"
