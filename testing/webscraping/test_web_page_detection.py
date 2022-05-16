from unittest import TestCase

from webScraping.WebPageDetection import if_url_belongs_to_company, if_url_has_company_reference, \
    get_company_and_ref_websites_urls_for_tag, get_company_website_urls, get_listed_leader_linkedin_page


class TestIf_url_belongs_to_company(TestCase):
    def test_if_url_belongs_to_company(self):
        self.assertTrue(if_url_belongs_to_company("google llc inc",("""https://www.google.com/""","google is a company")))

    def test_if_url_has_company_reference(self):
        self.assertTrue(if_url_has_company_reference("ford",("google.com", "ford is a good company")))

    def test_get_company_and_ref_websites_urls_for_tag(self):
        self.assertTrue("wellsfargo" in get_company_and_ref_websites_urls_for_tag("wellsfargo","diversity"))

    def test_get_company_website_urls(self):
        self.assertTrue("wellsfargo" in get_company_website_urls("wellsfargo"))

    def test_get_listed_leader_linkedin_page(self):
        self.assertTrue("linked" in get_listed_leader_linkedin_page("wellsfargo","carr"))

