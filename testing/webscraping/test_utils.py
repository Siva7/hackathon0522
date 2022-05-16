from unittest import TestCase
import requests
from webScraping.utils import text_from_html, get_visible_text_and_images_from_webpages, get_visible_text_from_webpages


class Test_utils(TestCase):
    def test_text_from_html(self):
        google_page = requests.get("https://www.google.com")
        google_page_text = text_from_html(google_page.text)
        print(google_page_text)
        self.assertTrue("Google" in google_page_text)

    def test_get_visible_text_and_images_from_webpages(self):
        leader_object=get_visible_text_and_images_from_webpages("https://www.google.com")
        self.assertTrue(not str(leader_object.text) == "")

    def test_get_visible_text_from_webpages(self):
        text = get_visible_text_from_webpages("https://www.google.com")
        self.assertTrue(not str(text) == "")