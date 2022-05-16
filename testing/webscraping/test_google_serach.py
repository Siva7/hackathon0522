from unittest import TestCase

from webScraping.GoogleSearch import google_search_results, google_search_results_and_desc


class TestGoogle_search_results_and_desc(TestCase):
    def test_google_search_results(self):
        google_result=str(google_search_results("google")[0])
        print(google_result)
        self.assertTrue("google.co.in" in google_result)

    def test_google_search_results_and_desc(self):
        google_search_url,google_search_desc=google_search_results_and_desc("google")[0]
        self.assertTrue("google" in str(google_search_url))
        print(str(google_search_desc))

